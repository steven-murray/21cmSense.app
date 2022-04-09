#
# views.py
#
import csv
import uuid
import base64

import binascii
import numpy as np
from flask import current_app, json, request

from . import api, models
from .calculation import *
from .models import *
from .schema import build_composite_schema, get_schema_descriptions_json, get_schema_groups, get_schema_names_json
from .redisfuncs import *


@api.route('/')
def welcome():
    """

    Returns
    -------
    string
        Welcome message
    """
    return 'Welcome to Project 43!'


@api.route('/ping')
def ping():
    """API ping test

    Returns
    -------
    json
        "pong"
    """
    return {
        "pong": "",
    }


@api.route('/users', methods=[HTTP_POST])
def create_user():
    """create a user for tracking models

    Parameters
    ----------
    username
        username

    Notes
    -----
    Expects json body of { "username":"the username" }

    Returns
    -------
    json::
        {
          "uuid": "unique uid",
          "username": "user name"
        }

    """
    if request.method == HTTP_POST:
        try:
            userid = str(uuid.uuid4())
            rdb.sadd(user_key(userid), '')
            return {'uuid': userid}, HTTP_CREATED
        except redis.ConnectionError:
            return {KW_ERROR: "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR


# As of Flask 1.1, the return statement will automatically jsonify a dictionary in the first return value.

# status_code = flask.Response(status=201)
# return status_code
#
# return Response("{'a':'b'}", status=201, mimetype='application/json')

# notfound = 404
# return xyz, notfound

# return Response(json.dumps({'Error': 'Error in payload'}),
# status=422,
# mimetype="application/json")


@api.route('/users/<userid>', methods=[HTTP_DELETE])
def delete_user(userid):
    try:
        # remove all model references for the user
        models = list(rdb.smembers(user_key(userid)))
        if models:
            rdb.delete(*models)
        # and remove the user
        rdb.delete(user_key(userid))
        return "", HTTP_NO_CONTENT
    except redis.ConnectionError:
        return {KW_ERROR: "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR


@api.route('/users/<userid>/models', methods=[HTTP_GET])
def list_models(userid):
    try:
        l = []
        keys = rdb.smembers(user_key(userid))

        # the user may have multiple entries, e.g., model:xyz, antpos:abc
        matches = [x for x in keys if tag_match(TAG_MODEL, x)]
        for m in matches:
            l.append({KW_MODELNAME: rdb.hget(m, KW_MODELNAME), KW_MODELID: strip_tag(m)})
        return {'uuid': userid, 'models': l}, HTTP_OK
    except redis.ConnectionError:
        return {KW_ERROR: "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR


def get_model_json(modelid):
    if not model_exists(modelid):
        return None, None
    # request for a model. Note we can't use hmget because pickled data cannot automatically
    # be utf-8 decoded
    name = rdb.hget(model_key(modelid), KW_MODELNAME)
    data = rpickle.hget(model_key(modelid), KW_DATA)

    if data:
        # recall that json payload is pickled into a string
        data = pickle.loads(data)
        return name, data
    else:
        return None, None


@api.route('/users/<userid>/models/<modelid>', methods=[HTTP_GET])
def model_get(userid, modelid):
    try:
        if not user_exists(userid):
            return "", HTTP_NOT_FOUND
        (name, data) = get_model_json(modelid)
        if data is not None:
            return {KW_MODELNAME: name, KW_DATA: data}, HTTP_OK
        else:
            return "", HTTP_NOT_FOUND
    except redis.ConnectionError:
        return {KW_ERROR: "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR


@api.route('/users/<userid>/models/<modelid>', methods=[HTTP_PUT])
def model_update(userid, modelid):
    try:
        if not user_exists(userid) or not model_exists(modelid):
            return "", HTTP_NOT_FOUND
        if not (request.is_json and request.json and KW_DATA in request.get_json()):
            return {KW_ERROR: 'missing request body or bad request'}, HTTP_BAD_REQUEST
        req = request.get_json()
        rdb.hset(model_key(modelid), KW_MODELNAME, req[KW_MODELNAME])
        rpickle.hset(model_key(modelid), KW_DATA, pickle.dumps(req[KW_DATA]))
    except redis.ConnectionError:
        return {KW_ERROR: "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR


@api.route('/users/<userid>/models/<modelid>', methods=[HTTP_DELETE])
def model_delete(userid, modelid):
    try:
        if not user_exists(userid) or not model_exists(modelid):
            return "", HTTP_NOT_FOUND

        # The model is stored in the user's set as "model:uuid"
        rdb.srem(user_key(userid), model_key(modelid))
        rdb.delete(model_key(modelid))
        return "", HTTP_NO_CONTENT
    except redis.ConnectionError:
        return {KW_ERROR: "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR


# accepts:
# {"modelname": "name of model"}
# returns:
# {KW_MODELID:modelid, "modelname": "name of model"}
@api.route('/users/<userid>/models', methods=[HTTP_POST])
def model_create(userid):
    try:
        # this user isn't registered...
        if not user_exists(userid):
            return "", HTTP_NOT_FOUND

        if request.is_json and request.json and KW_MODELNAME in request.get_json() and KW_DATA in request.get_json():
            json = request.get_json()
            modelid = str(uuid.uuid4())
            modelname = json[KW_MODELNAME]

            # if model name exists, return conflict error
            if entryname_exists(userid, modelname, TAG_MODEL):
                return {KW_ERROR: 'duplicate model name'}, HTTP_CONFLICT

            # create the model
            rdb.hset(model_key(modelid), KW_MODELNAME, modelname)
            rpickle.hset(model_key(modelid), KW_DATA, pickle.dumps(json[KW_DATA]))

            # add to the user's models
            rdb.sadd(user_key(userid), model_key(modelid))
            return {'userid': userid, KW_MODELID: modelid, KW_MODELNAME: modelname}, HTTP_CREATED
        else:
            return {KW_ERROR: 'missing request body or bad request'}, HTTP_BAD_REQUEST
    except redis.ConnectionError:
        return {KW_ERROR: "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR


@api.route('/users/<userid>/antpos', methods=[HTTP_GET])
def list_antpos(userid):
    """

    Parameters
    ----------
    userid

    Returns
    -------

    """
    try:
        l = []
        keys = rdb.smembers(user_key(userid))

        # the user may have multiple entries, e.g., model:xyz, antpos:abc
        matches = [x for x in keys if tag_match(TAG_ANTPOS, x)]

        for a in matches:
            l.append({KW_ANTPOSNAME: rdb.hget(a, KW_ANTPOSNAME), KW_ANTPOSID: strip_tag(a)})
        return {'uuid': userid, 'antpos': l}, HTTP_OK
    except redis.ConnectionError:
        return {KW_ERROR: "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR



@api.route('/users/<userid>/antpos/<antposid>', methods=[HTTP_GET])
def antpos_get(userid, antposid):
    """

    Parameters
    ----------
    userid
    antposid

    Returns
    -------

    """
    try:
        if not user_exists(userid):
            return "", HTTP_NOT_FOUND
        (name, data) = get_antpos_json(antposid)
        if data is not None:
            return {KW_ANTPOSNAME: name, KW_DATA: data}, HTTP_OK
        else:
            return "", HTTP_NOT_FOUND
    except redis.ConnectionError:
        return {KW_ERROR: "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR


@api.route('/users/<userid>/antpos/<antposid>', methods=[HTTP_PUT])
def antpos_update(userid, antposid):
    """

    Parameters
    ----------
    userid
    antposid

    Returns
    -------

    """
    try:
        if not user_exists(userid) or not antpos_exists(antposid):
            return "", HTTP_NOT_FOUND
        if not (request.is_json and request.json and KW_DATA in request.get_json()):
            return {KW_ERROR: 'missing request body or bad request'}, HTTP_BAD_REQUEST
        req = request.get_json()
        rdb.hset(antpos_key(antposid), KW_ANTPOSNAME, req[KW_ANTPOSNAME])
        rpickle.hset(antpos_key(antposid), KW_DATA, pickle.dumps(req[KW_DATA]))
    except redis.ConnectionError:
        return {KW_ERROR: "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR


@api.route('/users/<userid>/antpos/<antposid>', methods=[HTTP_DELETE])
def antpos_delete(userid, antposid):
    """

    Parameters
    ----------
    userid
    antposid

    Returns
    -------

    """
    try:
        if not user_exists(userid) or not antpos_exists(antposid):
            return "", HTTP_NOT_FOUND

        # The antpos model is stored in the user's set as "antpos:uuid"
        rdb.srem(user_key(userid), antpos_key(antposid))
        rdb.delete(antpos_key(antposid))
        return "", HTTP_NO_CONTENT
    except redis.ConnectionError:
        return {KW_ERROR: "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR


def translate_and_validate_antenna_data(data):
    """

    Parameters
    ----------
    thejson

    Returns
    -------

    """
    # data must be:
    # 1. base64 encoded
    # 2. comma-separated values
    # 3. either 2 or three values per line
    # 3a. if the third value is missing, it will be replaced by 0.0
    array2d = []

    try:
        s = base64.b64decode(data).decode('utf-8')
    except (UnicodeDecodeError, binascii.Error):
        return None

    # split our file into lines and put it in an iterable object (list)
    l = s.splitlines()

    # use the csv reader to parse it
    reader = csv.reader(l)
    for line in reader:

        # we must either have two or three values. All two-value lines have a third
        # value of 0.0 added
        if len(line) < 2 or len(line) > 3:
            return None
        try:

            # convert all string values to float
            numline = list(map(lambda x: float(x), line))
            if len(numline) == 2:
                numline.append(0.0)
        except ValueError:
            return None

        # build our 2-d array
        array2d.append(numline)

    return array2d


@api.route('/users/<userid>/antpos', methods=[HTTP_POST])
def antpos_create(userid):
    """

    Parameters
    ----------
    userid

    Returns
    -------

    """
    try:
        # this user isn't registered...
        if not user_exists(userid):
            return "", HTTP_NOT_FOUND

        if request.is_json and request.json and KW_ANTPOSNAME in request.get_json() and KW_DATA in request.get_json():
            json = request.get_json()
            antposid = str(uuid.uuid4())
            antposname = json[KW_ANTPOSNAME]

            # if antpos name exists, return conflict error
            if entryname_exists(userid, antposname, TAG_ANTPOS):
                return {KW_ERROR: 'duplicate antpos name'}, HTTP_CONFLICT

            # create the antpos entry
            rdb.hset(antpos_key(antposid), KW_ANTPOSNAME, antposname)

            array2d = translate_and_validate_antenna_data(json[KW_DATA])
            if array2d is None:
                return {KW_ERROR: "CSV file is improperly formatted. Please see documentation."}, \
                       HTTP_UNPROCESSABLE_ENTITY

            rpickle.hset(antpos_key(antposid), KW_DATA, pickle.dumps(array2d))

            # add to the user's antpos entries
            rdb.sadd(user_key(userid), antpos_key(antposid))
            return {'userid': userid, KW_ANTPOSID: antposid, KW_ANTPOSNAME: antposname}, HTTP_CREATED
        else:
            return {KW_ERROR: 'missing request body or bad request'}, HTTP_BAD_REQUEST
    except redis.ConnectionError:
        return {KW_ERROR: "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR


@api.route('/schema/<schemagroup>/descriptions')
def schema_descriptions(schemagroup):
    """Return a list of all of the schema in a schema group along with user-friendly descriptions

    Parameters
    ----------
    schemagroup
        name of schema group to return descriptions for

    Returns
    -------

    """
    return get_schema_descriptions_json(schemagroup)


@api.route('/customschema', methods=[HTTP_POST])
def api_return():
    """

    Returns
    -------
    A custom schema
    """
    if request.method == HTTP_POST:
        lst = get_schema_groups()

        # we should be posted something like:
        # { "location": "location.json", "beam": "GaussianBeam.json", "antenna": "hera.json" }

        if request.is_json and request.json:
            req = request.get_json()
            for schema_group in lst:
                if schema_group in req:
                    print("json return for component %s=" % schema_group, req[schema_group]);
            return build_composite_schema(req)


@api.route('/schema/<schemagroup>/get/<schemaname>')
def get_schema(schemagroup, schemaname):
    """Return a specific schema within a group

    Parameters
    ----------
    schemagroup
        Name of schema group for requested schema
    schemaname
        Name of schema to return

    Returns
    -------
    json
        JSON containing a specific schema file

    See Also
    --------
    test_get_schema
    test_get_nonexistent_schema
    test_get_nonexistent_schema_group
    """
    return current_app.send_static_file('schema/' + schemagroup + '/' + schemaname + '.json')


@api.route('/schema/<schemagroup>')
def get_schema_group(schemagroup):
    """List all of the schemas in a schema group

    Parameters
    ----------
    schemagroup

    See Also
    --------
    test_get_schema_group

    Returns
    -------
    json
        List all of the schemas in a schema group in JSON format

    """
    return get_schema_names_json(schemagroup)


@api.route('/schema', methods=[HTTP_GET])
def list_all_schema_groups():
    """List all supported schema groups

    See Also
    --------
    test_list_all_schema_groups

    Returns
    -------
    json
        List of all supported schema groups

    """
    lst = get_schema_groups()
    return jsonify(lst)


@api.route("/test", methods=[HTTP_GET, HTTP_POST])
def testtest():
    if request.is_json and request.json:
        thisjson = request.get_data()

        # req = request.get_json()

        schema = """
{
  "$schema": "http://json-schema.org/schema#",
  "type": "object",
  "properties": {
    "schema": {
      "type": "string"
    },
    "data": {
      "type": "object",
      "properties": {
        "antenna": {
          "type": "object",
          "properties": {
            "hex_num": {
              "type": "integer"
            },
            "separation": {
              "type": "number"
            },
            "dl": {
              "type": "number"
            }
          },
          "required": [
            "dl",
            "hex_num",
            "separation"
          ]
        },
        "beam": {
          "type": "object",
          "properties": {
            "class": {
              "type": "string"
            },
            "frequency": {
              "type": "number"
            },
            "dish_size": {
              "type": "number"
            }
          },
          "required": [
            "class",
            "dish_size",
            "frequency"
          ]
        },
        "location": {
            "type": "object",
            "properties": {
                "latitude": {
                  "type": "number"
                }
            }
        }
      },
      "required": [
        "antenna",
        "beam",
        "latitude"
      ]
    },
    "units": {
      "type": "object",
      "properties": {
        "antenna": {
          "type": "object",
          "properties": {
            "separation": {
              "type": "string"
            },
            "dl": {
              "type": "string"
            }
          },
          "required": [
            "dl",
            "separation"
          ]
        },
        "beam": {
          "type": "object",
          "properties": {
            "frequency": {
              "type": "string",
              "enum": [ "Hz", "Mhz" ]
            }
          },
          "required": [
            "frequency"
          ]
        },
        "location": {
          "type": "object",
          "properties": {
            "latitude": {
              "type": "string", 
              "enum": [ "deg", "rad" ]
            }
          },
          "required": [
            "latitude"
          ]
        }
      },
      "required": [
        "antenna",
        "beam",
        "location"
      ]
    }
  },
  "required": [
    "data",
    "schema",
    "units"
  ]
}
    """
        # print("type of schema=",type(schema))
        # ss='{"hello":"there"}'
        # sch=json.loads(ss)
        sch = json.loads(schema)
        v = models.Validator()
        req_json = request.get_json()
        if v.validate(sch, req_json):
            print("json validated")
        else:
            print("json failed validation")

        fact = models.Factory()
        sensitivity = fact.go(req_json)
        power_std = sensitivity.calculate_sensitivity_1d()

        for v in sensitivity.k1d:
            print("v.value=", v.value, ", type(v.value)=", type(v.value))
        for v in power_std:
            print("v.value=", v.value, ", type(v.value)=", type(v.value))
        z = zip([v.value for v in sensitivity.k1d], [v.value for v in power_std])
        print(z)
        d = dict(z)
        print("dict=", d)
        print(json.dumps(d))
        return json.dumps(d)

    return jsonify("test succeeded.")


@api.route("/21cm/model/<modelid>", methods=[HTTP_POST])
def call_21cm_with_model(modelid):
    if request.is_json and request.json:
        req = request.get_json()
        calc = req[KW_CALCULATION]
        (name, data) = get_model_json(modelid)
        if name is None:
            return {KW_ERROR: "Model does not exist", KW_MODELID: modelid}
        data[KW_CALCULATION] = calc
        return calculate(data)
    else:
        return {KW_ERROR: "Bad request body"}, HTTP_BAD_REQUEST


@api.route("/21cm", methods=[HTTP_POST])
def call_21cm():
    """Make a computation request to the 21cmSense library

    Returns
    -------
    json
        Response to front-end containing data for calculation, or error if input was not good
    """
    if request.is_json and request.json:
        req = request.get_json()

        return calculate(req)
    else:
        return {KW_ERROR: "request is not in json format"}, HTTP_BAD_REQUEST

    # if request.is_json and request.json:
    #     req = request.get_json()
    #     return build_composite_schema(req)
    # if 'calculation' not in req:
    #     return json_error("error", "no calculation key found in json")
    # else:
    # key = req['calculation']
    # calculation_factory = CalculationFactory()
    # if calculation_factory.knows(key):
    #     calc = calculation_factory.get(key)
    #     return_json = handle_output(calc)
    #     return return_json
    # else:
    #     return json_error("error", "unknown calculation type: " + key)


@api.route("/21cm_default", methods=[HTTP_GET, HTTP_POST])
def to_cm_if():
    sensitivity = PowerSpectrum(
        observation=Observation(
            observatory=Observatory(
                antpos=hera(hex_num=7, separation=14, dl=12.12, units="m"),
                beam=GaussianBeam(frequency=135.0, dish_size=14),
                latitude=38 * np.pi / 180.0
            )
        )
    )
    power_std = sensitivity.calculate_sensitivity_1d()
    sens = [v.value for v in sensitivity.k1d]
    powr = [v.value.tostring() for v in power_std]
    for v in power_std:
        print("v=", v.value, " and type=", type(v.value))
    print('sens=', sens)
    print('powr=', powr)
    z = zip([v.value for v in sensitivity.k1d], [v.value for v in power_std])
    print(z)
    print(json.dumps(z))
    return json.dumps(dict(z))
