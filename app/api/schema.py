#
# schema.py
#

import json
import os
from json import JSONDecodeError, JSONDecoder

from flask import current_app
from flask import jsonify

import jsonschema

from .json_util import json_error
from .util import DebugPrint

debug = DebugPrint(0).debug_print


# get a list of the schema names within a schema group
def get_schema_names(schemagroup):
    try:
        dirs = os.listdir(current_app.root_path + '/static/schema/' + schemagroup)
    except FileNotFoundError:
        return None
    schemas = [dir.replace('.json', '') for dir in dirs]
    return schemas


# get schema names in proper format for return to client
def get_schema_names_json(schemagroup):
    j = get_schema_names(schemagroup)
    if j is None:
        return jsonify(error="Schema group does not exist.", schemagroup=schemagroup)
    else:
        return jsonify(j)


# returns a list of all schemas in the provided schema group along with a textual description (appropriate for display
# in a user interface) of the schema
# ex:
# {
#   "1D-cut-of-2D-sensitivity": "1D cut of 2D sensitivity"
# }
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

    if not d:
        return json_error("error", "error returning data")
    else:
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
    debug("loaded schema=" + str(l), 9)
    return l


def load_schema_generic(schemadir: str, schemagroup: str, schemaname: str):
    try:
        p = "app/static/" + schemadir + "/" + schemagroup + "/" + schemaname + ".json"
        debug("going to load schema from path: " + p, 3)
        f = open("app/static/" + schemadir + "/" + schemagroup + "/" + schemaname + ".json", 'r')
        schema = json.load(f)
        f.close()
    except (JSONDecodeError, IOError) as e:
        print("error=", e)
        return None
    else:
        return schema


# pass a dict such as:
# { group: schema, [...] }
# ex: { "beam": "GaussianBeam", "location": "latitude", "antenna": "hera", "calculation": "baselines-distributions" }
# schema should already be a json object
def build_composite_schema(schema: JSONDecoder):
    # get calculation type
    if 'calculation' not in schema:
        return json_error("error", "specified schema missing 'calculation' key")

    calculation_type = schema['calculation']
    debug("Going to load schema for calculation " + calculation_type, 9)

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
        debug("Going to load component schema %s/%s" % (component, comp_schema_name), 3)
        newschema['data'][component] = load_schema(component, comp_schema_name)
        newschema['units'][component] = {}

    return jsonify(newschema)
    # d[schema_name] = sch['description']


class Validator:

    def __init__(self, thejson):
        self.thejson = thejson
        pass

    def valid_groups(self):
        """
        valid_groups determines if top-level json keywords are present

        :return:
        true if and only if only the required top level json groups are present.
        Fails if extra groups are present
        False if a required group is missing
        """
        self.error = False
        self.errorMsg = ""

        required = {'calculation', 'data', 'units'}
        supplied = set(self.thejson.keys())

        # sections provided but not allowed
        surplus = supplied - required
        if surplus:
            self.error = True
            self.errorMsg = "Surplus sections " + str(surplus)

        # sections required but not provided (note: takes precedence over surplus sections to
        #   simplify error reporting to client)
        missing = required - supplied
        if missing:
            self.error = True
            self.errorMsg = "Missing sections " + str(missing)

        # prettier but we've already calculated surplus and missing so ought to save the set operation
        # return required.intersection(supplied) == required
        return not (surplus or missing)

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

    # schema must be in JSON and compatible with provided schema rules
    def validate(self, schema, suppliedjson):
        # sch=json.loads(schema)
        # print("Schema=",sch)
        # sch=json.loads(schema)
        #        f = open("app/static/schema/hera-validation.json", 'r')
        f = open("app/static/validation-schema/hera-validation.json", 'r')
        sch = json.load(f)
        print("We got this json:", suppliedjson)
        try:
            jsonschema.validate(instance=suppliedjson, schema=sch)
            return suppliedjson
        except jsonschema.ValidationError as e:
            return None

    def load_schemafile(self, schema_name):

        pass
