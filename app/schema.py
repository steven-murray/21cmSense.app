import functools
import pickle
from json import JSONDecodeError, JSONDecoder

import pprint
# import jsonpickle


import os

import numpy
from flask import current_app
from flask import jsonify

# from .json_util import json_error
# from app.api.errors import error

import json
import jsonschema
from jsonschema import ValidationError
from py21cmsense import GaussianBeam, Observatory, Observation, PowerSpectrum, hera
# from .util import DebugPrint
# from ..utils.utils import get_unit_string

from hashlib import md5

def get_schema_names(schemagroup):
    try:
        dirs = os.listdir(current_app.root_path + '/static/schema/' + schemagroup)
    except FileNotFoundError:
        return None
    schemas = [dir.replace('.json', '') for dir in dirs]
    return schemas


def get_schema_descriptions_json(schemagroup):
    d = {}
    schema_names = get_schema_names(schemagroup)
    if schema_names is None:
        return json_error("error", "schema " + schemagroup + " not found.")

    for schema_name in get_schema_names(schemagroup):
        try:
            f = open("app/static/schema/" + schemagroup + "/" + schema_name + ".json", 'r')
            sch = json.load(f)
            f.close()
            d[schema_name] = sch['description']

        # issue with json.load()
        except JSONDecodeError:
            pass

        # issue with f.open()
        except OSError:
            pass

        # issue with finding 'description' key in json
        except KeyError:
            pass
    return jsonify(d)


def get_schema_groups():
    dirs = os.listdir(current_app.root_path + '/static/schema')
    # print("schema groups")
    # for dd in d:
    #     print(dd)
    return dirs


def get_schema_groups_json():
    d = get_schema_groups()
    j = {}
    j['required'] = list(d)
    return jsonify(j)


def load_schema(schemagroup: str, schemaname: str):
    l = load_schema_generic('schema', schemagroup, schemaname)
    print("loaded schema=", l)
    return l


def load_schema_generic(schemadir: str, schemagroup: str, schemaname: str):
    try:
        p = "app/static/" + schemadir + "/" + schemagroup + "/" + schemaname + ".json"
        print("going to load schema from path: ", p)
        f = open("app/static/" + schemadir + "/" + schemagroup + "/" + schemaname + ".json", 'r')
        schema = json.load(f)
        f.close()
    except (JSONDecodeError, IOError) as e:
        print("error=", e)
        return None
    else:
        return schema


# load a validation schema.  It must either have the same name as the schema that is to be validated, or
# be "default"
def load_validation_schema(schemagroup: str, schemaname: str):
    schema = load_schema_generic('validation-schema', schemagroup, schemaname)
    if not schema:
        schema = load_schema_generic('validation-schema', schemagroup, "default")
        if not schema:
            debug(1, "Cannot locate schema for %s/%s" % (schemagroup, schemaname))
            return None
    print("DEBUG: returning validation schema:", schema)
    return schema


def build_schema_for_validation(component, data_json, units_json):
    return {'data': {component: data_json[component]}, 'units': {component: units_json[component]}}
    # return d


# pass a dict such as:
# { group: schema, [...] }
# ex: { "beam": "GaussianBeam", "location": "latitude", "antenna": "hera", "calculation": "baselines-distributions" }
# schema should already be a json object
def build_composite_schema(schema: JSONDecoder):
    # get calculation type
    if 'calculation' not in schema:
        return json_error("error", "specified schema missing 'calculation' key")

    calculation_type = schema['calculation']
    print("Going to load schema for calculation ", calculation_type)

    calc_schema = load_schema('calculation', calculation_type)
    if not calc_schema:
        return json_error("error", "Cannot find requested calculation schema " + calculation_type)

    newschema = {"calculation": calculation_type, "data": {}, "units": {}}
    # if not jsonschema.validate(calc_schema, load_validation_schema('calculation', calculation_type)):
    #     return json_error("error", "Schema failed validation")
    for component in calc_schema['required']:
        if component not in schema:
            return json_error("error", "Missing required data component " + component)
        else:
            comp_schema_name = schema[component]
        # if component not in schema['data']:
        #     return json_error("error", "Missing required data component " + component)
        # if 'schema' not in schema['data'][component]:
        #     return json_error("error", "Missing schema identifier in data component " + component)
        # else:
        #     comp_schema_name = schema['data'][component]['schema']

        # cs=build_schema_for_validation(schema['data'][component], schema['units'][component])

        #
        #
        # Validation, save for later
        # cs = build_schema_for_validation(component, schema['data'], schema['units'])
        # print("Going to validate schema: ", cs)
        # validation_schema = load_validation_schema(component, comp_schema_name)
        # if not validation_schema:
        #     return json_error("error",
        #                       "Cannot locate validation schema for schema %s/%s" % (component, comp_schema_name))
        # try:
        #     jsonschema.validate(cs, validation_schema)
        # except ValidationError:
        #     return json_error("error", "Cannot validate schema %s/%s" % (component, comp_schema_name))
        print("Going to load component schema %s/%s" % (component, comp_schema_name))
        newschema['data'][component] = load_schema(component, comp_schema_name)
        newschema['units'][component] = {}

    return jsonify(newschema)
    # d[schema_name] = sch['description']
