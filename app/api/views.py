#
# views.py
#
# Project 43 - Web Application for Radio Astronomy Sensitivity
# Author: Brian Pape
# Revision: 0.1
#
# This module contains Flask RESTful API call (view) support

import base64
import binascii
import csv
import pickle
import uuid
from typing import Tuple

from flask import current_app, jsonify, request
from py21cmsense import PowerSpectrum

from . import api
from . import calculation as calc
from . import constants as cnst
from . import redisfuncs as rd
from .schema import (
    build_composite_schema,
    get_schema_descriptions_json,
    get_schema_groups,
    get_schema_names_json,
)


def ensure_redis_available(fnc):
    def inner(*args, **kwargs):
        try:
            return fnc(*args, **kwargs)
        except rd.redis.ConnectionError:
            return {
                rd.KW_ERROR: "rd.redis database unavailable"
            }, cnst.HTTP_INTERNAL_SERVER_ERROR

    return inner


@api.route("/")
def welcome():
    """

    Returns
    -------
    string
        Welcome message
    """
    return "Welcome to 21cmSense.app!"


@api.route("/ping")
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


@api.route("/users", methods=["POST"])
@ensure_redis_available
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
    userid = str(uuid.uuid4())
    rd.rdb.sadd(rd.user_key(userid), "")
    return {"uuid": userid}, cnst.HTTP_CREATED


@api.route("/users/<userid>", methods=[cnst.HTTP_DELETE])
@ensure_redis_available
def delete_user(userid):
    # remove all model references for the user
    models = list(rd.rdb.smembers(rd.user_key(userid)))
    if models:
        rd.rdb.delete(*models)
    # and remove the user
    rd.rdb.delete(rd.user_key(userid))
    return "", cnst.HTTP_NO_CONTENT


@api.route("/users/<userid>/models", methods=[cnst.HTTP_GET])
@ensure_redis_available
def list_models(userid):
    models = []
    keys = rd.rdb.smembers(rd.user_key(userid))

    # the user may have multiple entries, e.g., model:xyz, antpos:abc
    matches = [x for x in keys if rd.tag_match(rd.TAG_MODEL, x)]
    for m in matches:
        models.append(
            {
                rd.KW_MODELNAME: rd.rdb.hget(m, rd.KW_MODELNAME),
                rd.KW_MODELID: rd.strip_tag(m),
            }
        )
    return {"uuid": userid, "models": models}, cnst.HTTP_OK


class NonExistentModel(RuntimeError):
    pass


def get_model_data(modelid) -> Tuple[str, PowerSpectrum, dict]:
    if not rd.model_exists(modelid):
        raise NonExistentModel()

    # request for a model. Note we can't use hmget because pickled data cannot automatically
    # be utf-8 decoded
    name = rd.rdb.hget(rd.model_key(modelid), rd.KW_MODELNAME)
    data = rd.rpickle.hget(rd.model_key(modelid), rd.KW_DATA)
    params = rd.rpickle.hget(rd.model_key(modelid), rd.KW_MODELPARAMS)

    data = pickle.loads(data)
    params = pickle.loads(params)

    return name, data, params


@api.route("/users/<userid>/models/<modelid>", methods=[cnst.HTTP_GET])
@ensure_redis_available
def model_get(userid, modelid):
    if not rd.user_exists(userid):
        return "", cnst.HTTP_NOT_FOUND

    try:
        name, pspec, params = get_model_data(modelid)
        return {
            rd.KW_MODELNAME: name,
            rd.KW_DATA: pspec,
            rd.KW_MODELPARAMS: params,
        }, cnst.HTTP_OK
    except NonExistentModel:
        return "", cnst.HTTP_NOT_FOUND


@api.route("/users/<userid>/models/<modelid>", methods=[cnst.HTTP_PUT])
@ensure_redis_available
def model_update(userid, modelid):
    if not rd.user_exists(userid) or not rd.model_exists(modelid):
        return "", cnst.HTTP_NOT_FOUND
    if not (request.is_json and request.json and rd.KW_DATA in request.get_json()):
        return {
            rd.KW_ERROR: "missing request body or bad request"
        }, cnst.HTTP_BAD_REQUEST

    json = request.get_json()

    name, old_pspec, old_params = get_model_data(modelid)

    pspec = calc.update_pspec_from_json(old_pspec, json[rd.KW_DATA], old_params)

    rd.rdb.hset(rd.model_key(modelid), rd.KW_MODELNAME, json[rd.KW_MODELNAME])
    rd.rpickle.hset(rd.model_key(modelid), rd.KW_DATA, pickle.dumps(pspec))
    rd.rpickle.hset(
        rd.model_key(modelid), rd.KW_MODELPARAMS, pickle.dumps(json[rd.KW_DATA])
    )


@api.route("/users/<userid>/models/<modelid>", methods=[cnst.HTTP_DELETE])
@ensure_redis_available
def model_delete(userid, modelid):
    if not rd.user_exists(userid) or not rd.model_exists(modelid):
        return "", cnst.HTTP_NOT_FOUND

    # The model is stored in the user's set as "model:uuid"
    rd.rdb.srem(rd.user_key(userid), rd.model_key(modelid))
    rd.rdb.delete(rd.model_key(modelid))

    return "", cnst.HTTP_NO_CONTENT


@api.route("/users/<userid>/models", methods=["POST"])
@ensure_redis_available
def model_create(userid):
    # this user isn't registered...
    if not rd.user_exists(userid):
        return "", cnst.HTTP_NOT_FOUND

    if (
        request.is_json
        and request.json
        and rd.KW_MODELNAME in request.get_json()
        and rd.KW_DATA in request.get_json()
    ):
        json = request.get_json()
        modelid = str(uuid.uuid4())
        modelname = json[rd.KW_MODELNAME]

        # if model name exists, return conflict error
        if rd.entryname_exists(userid, modelname, rd.TAG_MODEL):
            return {rd.KW_ERROR: "duplicate model name"}, cnst.HTTP_CONFLICT

        # create the model
        pspec = calc.json_to_power_spectrum(json[rd.KW_DATA])

        rd.rdb.hset(rd.model_key(modelid), rd.KW_MODELNAME, modelname)
        rd.rpickle.hset(rd.model_key(modelid), rd.KW_DATA, pickle.dumps(pspec))
        rd.rpickle.hset(rd.model_key(modelid), rd.KW_DATA, pickle.dumps(json))

        # add to the user's models
        rd.rdb.sadd(rd.user_key(userid), rd.model_key(modelid))
        return {
            "userid": userid,
            rd.KW_MODELID: modelid,
            rd.KW_MODELNAME: modelname,
        }, cnst.HTTP_CREATED
    else:
        return {
            rd.KW_ERROR: "missing request body or bad request"
        }, cnst.HTTP_BAD_REQUEST


@api.route("/users/<userid>/antpos", methods=[cnst.HTTP_GET])
@ensure_redis_available
def list_antpos(userid):
    """

    Parameters
    ----------
    userid

    Returns
    -------

    """
    models = []
    keys = rd.rdb.smembers(rd.user_key(userid))

    # the user may have multiple entries, e.g., model:xyz, antpos:abc
    matches = [x for x in keys if rd.tag_match(rd.TAG_ANTPOS, x)]

    for a in matches:
        models.append(
            {
                rd.KW_ANTPOSNAME: rd.rdb.hget(a, rd.KW_ANTPOSNAME),
                rd.KW_ANTPOSID: rd.strip_tag(a),
            }
        )
    return {"uuid": userid, "antpos": models}, cnst.HTTP_OK


@api.route("/users/<userid>/antpos/<antposid>", methods=[cnst.HTTP_GET])
@ensure_redis_available
def antpos_get(userid, antposid):
    """

    Parameters
    ----------
    userid
    antposid

    Returns
    -------

    """
    if not rd.user_exists(userid):
        return "", cnst.HTTP_NOT_FOUND
    (name, data) = rd.get_antpos_json(antposid)
    if data is not None:
        return {rd.KW_ANTPOSNAME: name, rd.KW_DATA: data}, cnst.HTTP_OK
    else:
        return "", cnst.HTTP_NOT_FOUND


@api.route("/users/<userid>/antpos/<antposid>", methods=[cnst.HTTP_PUT])
@ensure_redis_available
def antpos_update(userid, antposid):
    """

    Parameters
    ----------
    userid
    antposid

    Returns
    -------

    """
    if not rd.user_exists(userid) or not rd.antpos_exists(antposid):
        return "", cnst.HTTP_NOT_FOUND
    if not (request.is_json and request.json and rd.KW_DATA in request.get_json()):
        return {
            rd.KW_ERROR: "missing request body or bad request"
        }, cnst.HTTP_BAD_REQUEST
    req = request.get_json()
    rd.rdb.hset(rd.antpos_key(antposid), rd.KW_ANTPOSNAME, req[rd.KW_ANTPOSNAME])
    rd.rpickle.hset(rd.antpos_key(antposid), rd.KW_DATA, pickle.dumps(req[rd.KW_DATA]))


@api.route("/users/<userid>/antpos/<antposid>", methods=[cnst.HTTP_DELETE])
@ensure_redis_available
def antpos_delete(userid, antposid):
    """

    Parameters
    ----------
    userid
    antposid

    Returns
    -------

    """
    if not rd.user_exists(userid) or not rd.antpos_exists(antposid):
        return "", cnst.HTTP_NOT_FOUND

    # The antpos model is stored in the user's set as "antpos:uuid"
    rd.rdb.srem(rd.user_key(userid), rd.antpos_key(antposid))
    rd.rdb.delete(rd.antpos_key(antposid))
    return "", cnst.HTTP_NO_CONTENT


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
        s = base64.b64decode(data).decode("utf-8")
    except (UnicodeDecodeError, binascii.Error):
        return None

    # split our file into lines and put it in an iterable object (list)
    ln = s.splitlines()

    # use the csv reader to parse it
    reader = csv.reader(ln)
    for line in reader:

        # we must either have two or three values. All two-value lines have a third
        # value of 0.0 added
        if len(line) < 2 or len(line) > 3:
            return None
        try:

            # convert all string values to float
            numline = [float(x) for x in line]
            if len(numline) == 2:
                numline.append(0.0)
        except ValueError:
            return None

        # build our 2-d array
        array2d.append(numline)

    return array2d


@api.route("/users/<userid>/antpos", methods=["POST"])
@ensure_redis_available
def antpos_create(userid):
    """

    Parameters
    ----------
    userid

    Returns
    -------

    """
    # this user isn't registered...
    if not rd.user_exists(userid):
        return "", cnst.HTTP_NOT_FOUND

    if (
        request.is_json
        and request.json
        and rd.KW_ANTPOSNAME in request.get_json()
        and rd.KW_DATA in request.get_json()
    ):
        json = request.get_json()
        antposid = str(uuid.uuid4())
        antposname = json[rd.KW_ANTPOSNAME]

        # if antpos name exists, return conflict error
        if rd.entryname_exists(userid, antposname, rd.TAG_ANTPOS):
            return {rd.KW_ERROR: "duplicate antpos name"}, cnst.HTTP_CONFLICT

        # create the antpos entry
        rd.rdb.hset(rd.antpos_key(antposid), rd.KW_ANTPOSNAME, antposname)

        array2d = translate_and_validate_antenna_data(json[rd.KW_DATA])
        if array2d is None:
            return {
                rd.KW_ERROR: "CSV file is improperly formatted. Please see documentation."
            }, cnst.HTTP_UNPROCESSABLE_ENTITY

        rd.rpickle.hset(rd.antpos_key(antposid), rd.KW_DATA, pickle.dumps(array2d))

        # add to the user's antpos entries
        rd.rdb.sadd(rd.user_key(userid), rd.antpos_key(antposid))
        return {
            "userid": userid,
            rd.KW_ANTPOSID: antposid,
            rd.KW_ANTPOSNAME: antposname,
        }, cnst.HTTP_CREATED
    else:
        return {
            rd.KW_ERROR: "missing request body or bad request"
        }, cnst.HTTP_BAD_REQUEST


@api.route("/schema/<schemagroup>/descriptions")
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


@api.route("/schema/<schemagroup>/get/<schemaname>")
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
    return current_app.send_static_file(
        "schema/" + schemagroup + "/" + schemaname + ".json"
    )


@api.route("/schema/<schemagroup>")
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


@api.route("/schema", methods=[cnst.HTTP_GET])
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


@api.route("/21cm/model/<modelid>", methods=["POST"])
def call_21cm_with_model(modelid):
    if request.is_json and request.json:
        req = request.get_json()
        calc = req[rd.KW_CALCULATION]
        name, data, json = get_model_data(modelid)
        if name is None:
            return {rd.KW_ERROR: "Model does not exist", rd.KW_MODELID: modelid}
        data[rd.KW_CALCULATION] = calc
        return calc.calculate(data)
    else:
        return {rd.KW_ERROR: "Bad request body"}, cnst.HTTP_BAD_REQUEST


@api.route("/21cm", methods=["POST"])
def call_21cm():
    """Make a computation request to the 21cmSense library

    Returns
    -------
    json
        Response to front-end containing data for calculation, or error if input was not good
    """
    if request.is_json and request.json:
        req = request.get_json()

        return calc.calculate(req)
    else:
        return {rd.KW_ERROR: "request is not in json format"}, cnst.HTTP_BAD_REQUEST
