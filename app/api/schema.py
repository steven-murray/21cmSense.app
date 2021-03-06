#
# schema.py
#
# Project 43 - Web Application for Radio Astronomy Sensitivity
# Author: Brian Pape
# Revision: 0.1
#
# This module contains json schema support and validation

import json
import logging
import os
from json import JSONDecodeError, JSONDecoder

import jsonschema
from flask import current_app, jsonify

from .constants import SCHEMA_REL_DIR
from .exceptions import ValidationException
from .json_util import json_error

logger = logging.getLogger(__name__)


def get_schema_names(schemagroup):
    """get a list of the schema names within a schema group

    Parameters
    ----------
    schemagroup
        Schema group to check
    Returns
    -------
    list
        List of schema within the specified schema group

    """
    try:
        dirs = os.listdir(current_app.root_path + "/static/schema/" + schemagroup)
    except FileNotFoundError:
        return None
    schemas = [d.replace(".json", "") for d in dirs]
    return schemas


def get_schema_names_json(schemagroup):
    """get schema names in proper format for return to client

    Parameters
    ----------
    schemagroup
        Schema group to check

    Returns
    -------
    json
        List of schema within specified schema group (for return to client)

    """
    j = get_schema_names(schemagroup)
    if j is None:
        return jsonify(error="Schema group does not exist.", schemagroup=schemagroup)
    else:
        return jsonify(j)


def get_schema_descriptions_json(schemagroup):
    """returns a list of all schemas in the provided schema group along with a textual description
        of the schema

    The list is appropriate for display in a user interface

    Examples
    ________
    Example::

        {
            '1D-cut-of-2D-sensitivity: '1D cut of 2D sensitivity'
        }

    Parameters
    ----------
    schemagroup
        Schema group to check

    Returns
    -------
    json
        Textual list of all schemas in provided schemagroup

    """
    d = {}
    schema_names = get_schema_names(schemagroup)
    if schema_names is None:
        return json_error("error", "schema " + schemagroup + " not found.")

    for schema_name in get_schema_names(schemagroup):
        try:
            f = open("app/static/schema/" + schemagroup + "/" + schema_name + ".json")
            sch = json.load(f)
            f.close()
            d[schema_name] = sch["description"]

        # issue with json.load()
        except JSONDecodeError:
            pass

        # issue with f.open()
        except OSError:
            pass

        # issue with finding 'description' key in json
        except KeyError:
            pass

    if not d:
        return json_error("error", "error returning data")
    else:
        return jsonify(d)


def get_schema_groups():
    """List all all available schema groups

    Returns
    -------
    list
        List of available schema groups

    """
    dirs = os.listdir(current_app.root_path + "/static/schema")
    return dirs


def get_schema_groups_json():
    """List of all available schema groups

    Returns
    -------
    json
        List of available schema groups

    """
    d = get_schema_groups()
    j = {}
    j["required"] = list(d)
    return jsonify(j)


def load_schema(schemagroup: str, schemaname: str):
    """Load schema from persistent storage

    Parameters
    ----------
    schemagroup
        Group for schema file
    schemaname
        Schema within group

    Returns
    -------
    json
        Contents of requested schema file or None if file does not exist

    """
    return load_schema_generic("schema", schemagroup, schemaname)


def load_schema_generic(schemadir: str, schemagroup: str, schemaname: str):
    """

    Parameters
    ----------
    schemadir
        Static filesystem location for schema files, relative to app package
    schemagroup
        Group for schema file
    schemaname
        Schema within group

    Returns
    -------
    json
        Contents of requested schema file or None if file does not exist

    """
    try:
        p = SCHEMA_REL_DIR + schemadir + "/" + schemagroup + "/" + schemaname + ".json"
        with open(p) as fl:
            schema = json.load(fl)
        return schema

    except (JSONDecodeError, OSError) as e:
        logger.error(e)


def build_composite_schema(schema: JSONDecoder):
    """Build a composite schema from parts based on a JSON request

    Parameters
    ----------
    schema
        JSON dictionary containing the schema groups and schema files desired in composite schema

    Notes
    -----
    pass a dict such as:
    { group: schema, [...] }
    ex: { "beam": "GaussianBeam", "location": "latitude", "antenna": "hera", "calculation": "baselines-distributions" }
    schema should already be a json object

    Returns
    -------
    json
        json schema object or json formatted error if request was invalid

    """
    # get calculation type
    if "calculation" not in schema:
        return json_error("error", "specified schema missing 'calculation' key")

    calculation_type = schema["calculation"]

    calc_schema = load_schema("calculation", calculation_type)
    if not calc_schema:
        return json_error(
            "error", "Cannot find requested calculation schema " + calculation_type
        )

    newschema = {"calculation": calculation_type, "data": {}, "units": {}}
    # if not jsonschema.validate(calc_schema, load_validation_schema('calculation', calculation_type)):
    #     return json_error("error", "Schema failed validation")
    for component in calc_schema["required"]:
        if component not in schema:
            return json_error("error", "Missing required data component " + component)
        else:
            comp_schema_name = schema[component]
        newschema["data"][component] = load_schema(component, comp_schema_name)
        newschema["units"][component] = {}

    return jsonify(newschema)
    # d[schema_name] = sch['description']


class Validator:
    """Validate a submitted JSON schema prior to using for calculation"""

    def __init__(self, thejson):
        self.thejson = thejson

    def valid_groups(self):
        """valid_groups determines if top-level json keywords are present

        Returns
        -------
        bool
            true if and only if only the required top level json groups are present.
            Fails if extra groups are present
            False if a required group is missing

        Notes
        -----
        Raises ValidationException if validation fails
        """

        required = {"calculation", "data", "units"}
        supplied = set(self.thejson.keys())

        # sections provided but not allowed
        surplus = supplied - required
        if surplus:
            raise ValidationException("Surplus sections " + str(surplus))

        # sections required but not provided (note: takes precedence over surplus sections to
        #   simplify error reporting to client)
        missing = required - supplied
        if missing:
            raise ValidationException("Missing sections " + str(missing))

        # prettier but we've already calculated surplus and missing so ought to save the set operation
        # return required.intersection(supplied) == required
        return not (surplus or missing)

    # TODO
    # we need to ensure all of the required sections are present in this json
    # then we need to break it apart (e.g., antenna, beam, location) and verify each of those
    # sections against their individual validation schemas
    def valid_sections(self):
        """Ensure required sections are valid and present in the supplied json

        Returns
        -------
        bool
            True if valid, raises ValidationException is not validatable

        Notes
        -----
        If returning false, also sets 'error' to True and errorMsg to a message
        """
        data = self.thejson["data"]
        units = self.thejson["units"]
        for schemagroup in ["antenna", "beam", "location"]:
            j = self.build_schema_for_validation(schemagroup, data, units)
            if "schema" not in data[schemagroup]:
                raise ValidationException(
                    "Schema group section %s missing 'schema' keyword" % schemagroup
                )

            schemaname = data[schemagroup]["schema"]

            validation_schema = self.load_validation_schema(schemagroup, schemaname)
            if validation_schema is None:
                raise ValidationException(
                    "Validation schema not found for schema group="
                    + schemagroup
                    + ", schema="
                    + schemaname
                )

            if not self.validate(validation_schema, j):
                raise ValidationException(
                    "Error validating schemagroup section %s" % schemagroup
                )

        return True

    # load a validation schema.  It must either have the same name as the schema that is to be validated, or
    # be "default"
    def load_validation_schema(self, schemagroup: str, schemaname: str):
        """Load a validation schema from disk based on schema group and name

        Parameters
        ----------
        schemagroup - the schema group to search
        schemaname - the schema name to load

        Returns
        -------
        json
            The requested validation schema, or None if not found

        """
        schema = load_schema_generic("validation-schema", schemagroup, schemaname)
        if not schema:
            schema = load_schema_generic("validation-schema", schemagroup, "default")
            if not schema:
                return None
        # print("DEBUG: returning validation schema:", schema)
        return schema

    def build_schema_for_validation(self, schemagroup, data_json, units_json):
        """Build a schema for validation

        Parameters
        ----------
        schemagroup
            The schema group to use (e.g., 'antenna')
        data_json
            The data portion of the supplied json
        units_json
            The units portion of the supplied json

        Returns
        -------
        dict
            a dictionary (json) suitable for validating

        """
        return {
            "data": {schemagroup: data_json[schemagroup]},
            "units": {schemagroup: units_json[schemagroup]},
        }

    # schema must be in JSON and compatible with provided schema rules
    def validate(self, schema, suppliedjson):
        """Validate supplied schema against JSON Schema Specification-compliant validation schema

        Parameters
        ----------
        schema
        suppliedjson

        Returns
        -------
        bool
            True if validates, False otherwise

        """
        try:
            jsonschema.validate(instance=suppliedjson, schema=schema)
            return True
        except jsonschema.ValidationError as e:
            logger.error(e)
            return False
