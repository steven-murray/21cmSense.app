#
# views.py
#
import numpy as np
from flask import current_app, json, request

from . import api, models
from .json_util import json_error
from .models import *
from .calculation import *
import redis
import uuid

from .schema import build_composite_schema, get_schema_descriptions_json, get_schema_groups, get_schema_names_json

r = redis.Redis(decode_responses=True)
rpickle = redis.Redis(decode_responses=False)
# try:
#     r.ping()
# except ConnectionError:
#     return {"error":"redis database not available"}, HTTP_INTERNAL_SERVER_ERROR


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


# redis cache the model

# r=redis.Redis()
# u=username_hash
# m=modelname_hash
# p = pickle.dumps(json_dict)
# all of a user's models
# key to a set="user:"+userIDhash = "model:modelIDhash"
# (r.sadd (userkey, modelstring)
# a model is a hash with two entries: name and data
# r.hmset('model:'+modelnum, 'modelname', 'the name of the model')
# r.hmset('model:'+modelnum, 'data', '{json for this model}')
# key=u+":"+m
# r.set(key,p)
# return: pickle.loads(r.get(key))

def user_key(userid: str) -> str:
    return "user" + ":" + userid


def model_key(modelid: str) -> str:
    return "model" + ":" + modelid


def strip_tag(key: str) -> str:
    """

    Parameters
    ----------
    key
        tag:data key from redis

    Returns
    -------
    str
        data portion only
    """
    return key.split(':')[1]


def user_exists(userid):
    if r.exists(user_key(userid)):
        return True
    else:
        return False


def model_exists(modelid):
    if r.exists(model_key(modelid)):
        return True
    else:
        return False


def modelname_exists(userid, modelname):
    models = r.smembers(user_key(userid))
    for m in models:
        if r.hget(model_key(m), 'modelname') == modelname:
            return True

    return False


@api.route('/users', methods=['POST'])
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
    if request.method == 'POST':
        try:
            userid = str(uuid.uuid4())
            r.sadd(user_key(userid), '')
            return {'uuid': userid}, HTTP_CREATED
        except redis.ConnectionError:
            return {"error": "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR


# As of Flask 1.1, the return statement will automatically jsonify a dictionary in the first return value.

# status_code = flask.Response(status=201)
# return status_code
#
# return Response("{'a':'b'}", status=201, mimetype='application/json')

# notfound = 404
# return xyz, notfound

# return html_page_str, 200, {'ContentType': 'text/html'}
# return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# return Response(json.dumps({'Error': 'Error in payload'}),
# status=422,
# mimetype="application/json")


@api.route('/users/<userid>', methods=['DELETE'])
def delete_user(userid):
    try:
        # remove all model references for the user
        models = list(r.smembers(user_key(userid)))
        if models:
            r.delete(*models)
        # and remove the user
        r.delete(user_key(userid))
        return "", HTTP_NO_CONTENT
    except redis.ConnectionError:
        return {"error": "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR


@api.route('/users/<userid>/models', methods=['GET'])
def list_models(userid):
    try:
        l = []
        models = r.smembers(user_key(userid))
        for m in models:
            # don't return the empty model used as a set placeholder for the userid key
            if m:
                l.append({'modelname': r.hget(model_key(m), 'modelname'), 'modelid': m})
        return {'models': l}, HTTP_OK
    except redis.ConnectionError:
        return {"error": "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR


def get_model_json(modelid):
    if not model_exists(modelid):
        return None, None
    # request for a model. Note we can't use hmget because pickled data cannot automatically
    # be utf-8 decoded
    name = r.hget(model_key(modelid), 'modelname')
    data = rpickle.hget(model_key(modelid), 'data')

    if data:
        # recall that json payload is pickled into a string
        data = pickle.loads(data)
        return name, data
    else:
        return None, None


@api.route('/users/<userid>/models/<modelid>', methods=['GET'])
def model_get(userid, modelid):
    try:
        if not user_exists(userid):
            return "", HTTP_NOT_FOUND
        (name, data) = get_model_json(modelid)
        if data is not None:
            return {'modelname': name, 'data': data}, HTTP_OK
        else:
            return "", HTTP_NOT_FOUND
    except redis.ConnectionError:
        return {"error": "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR


@api.route('/users/<userid>/models/<modelid>', methods=['PUT'])
def model_update(userid, modelid):
    try:
        if not user_exists(userid) or not model_exists(modelid):
            return "", HTTP_NOT_FOUND
        if not (request.is_json and request.json and 'data' in request.get_json()):
            return {'error': 'missing request body or bad request'}, HTTP_BAD_REQUEST
        req = request.get_json()
        r.hset(model_key(modelid), 'modelname', req['modelname'])
        rpickle.hset(model_key(modelid), 'data', pickle.dumps(req['data']))
    except redis.ConnectionError:
        return {"error": "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR


@api.route('/users/<userid>/models/<modelid>', methods=['DELETE'])
def model_delete(userid, modelid):
    try:
        if not user_exists(userid) or not model_exists(modelid):
            return "", HTTP_NOT_FOUND
        r.srem(user_key(userid), modelid)
        r.delete(model_key(modelid))
        return "", HTTP_NO_CONTENT
    except redis.ConnectionError:
        return {"error": "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR


# accepts:
# {'modelname':'modelname'}
# returns:
# {'modelid':modelid, 'modelname':'modelname'}
@api.route('/users/<userid>/models', methods=['POST'])
def create_model(userid):
    try:
        # this user isn't registered...
        if not user_exists(userid):
            return "", HTTP_NOT_FOUND

        if request.is_json and request.json and 'modelname' in request.get_json() and 'data' in request.get_json():
            json = request.get_json()
            modelid = str(uuid.uuid4())
            modelname = json['modelname']

            # if model name exists, return conflict error
            if modelname_exists(userid, modelname):
                return {'error': 'duplicate model name'}, HTTP_CONFLICT

            # create the model
            r.hset(model_key(modelid), 'modelname', modelname)
            rpickle.hset(model_key(modelid), 'data', pickle.dumps(json['data']))

            # add to the user's models
            r.sadd(user_key(userid), modelid)
            return {'userid': userid, 'modelid': modelid, 'modelname': modelname}, HTTP_CREATED
        else:
            return {'error': 'missing request body or bad request'}, HTTP_BAD_REQUEST
    except redis.ConnectionError:
        return {"error": "redis database unavailable"}, HTTP_INTERNAL_SERVER_ERROR


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


@api.route('/customschema', methods=['POST'])
def api_return():
    """

    Returns
    -------
    A custom schema
    """
    if request.method == 'POST':
        lst = models.get_schema_groups()

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


@api.route('/schema', methods=['GET'])
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


@api.route("/test", methods=['GET', 'POST'])
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


@api.route("/21cm/model/<modelid>", methods=['POST'])
def call_21cm_with_model(modelid):
    if request.is_json and request.json:
        req = request.get_json()
        calc = req[KW_CALCULATION]
        (name, data) = get_model_json(modelid)
        if name is None:
            return {"error": "Model does not exist", "modelid": modelid}
        data[KW_CALCULATION] = calc
        return calculate(data)
    else:
        return json_error("error", "Bad request body")


@api.route("/21cm", methods=['POST'])
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
        return json_error("error", "request is not in json format")

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


@api.route("/21cm_default", methods=['GET', 'POST'])
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
