#
# redisfuncs.py
#
# Project 43 - Web Application for Radio Astronomy Sensitivity
# Author: Brian Pape
# Revision: 0.1
#
# This module contains support for a redis database to store model and
# antenna position data (see API for reference)

import pickle

import redis

# tags used for redis namespaces
TAG_USER = "user"
TAG_MODEL = "model"
TAG_ANTPOS = "antpos"


# keywords used in JSON requests and responses
KW_DATA = "data"
KW_MODELID = "modelid"
KW_MODELNAME = "modelname"
KW_ID = "id"
KW_NAME = "name"
KW_MODELPARAMS = "modelparams"

KW_ANTPOSID = "antposid"
KW_ANTPOSNAME = "antposname"

KW_CALCULATION = "calculation"
KW_ERROR = "error"


# persistent redis database connection with automatic UTF-8 decoding
rdb = redis.Redis(decode_responses=True)

# automatic UTF-8 decoding is not compatible with pickled strings.
rpickle = redis.Redis(decode_responses=False)


# returns a redis key (namespace:identifier)
def user_key(userid: str) -> str:
    return TAG_USER + ":" + userid


# returns a redis key (namespace:identifier)
def model_key(modelid: str) -> str:
    return TAG_MODEL + ":" + modelid


# returns a redis key (namespace:identifier)
def antpos_key(antposid: str) -> str:
    return TAG_ANTPOS + ":" + antposid


# does user with provided userid exist?
def user_exists(userid):
    return rdb.exists(user_key(userid))


# does model with provided modelid exist?
def model_exists(modelid):
    return rdb.exists(model_key(modelid))


# does antpos data with provided antposid exist?
def antpos_exists(antposid):
    return rdb.exists(antpos_key(antposid))


def entryname_exists(userid, entryname, namespace) -> bool:
    """Whether a redis hash object of namespace 'namespace' and the
    'name' field of 'entryname' exists for the user with user ID 'userid'.

    Parameters
    ----------
    userid
    entryname
    namespace

    Returns
    -------

    """
    entries = rdb.smembers(user_key(userid))
    for m in entries:

        # ensure entry's tag matches and its name matches.  If the namespace is
        # e.g., 'model' then we expect the 'name' to be a field called 'modelname'.
        # this is done to eliminate constant switching between 'name' in the database
        # and 'modelname' in the submitted or return json.
        if tag_match(namespace, m) and rdb.hget(m, namespace + KW_NAME) == entryname:
            return True
    return False


def get_tag(key: str) -> str:
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
    k = key.split(":")
    if len(k) == 2:
        return k[0]
    else:
        return "INVALID"


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
    k = key.split(":")
    if len(k) == 2:
        return k[1]
    else:
        return k[0]


def tag_match(tag: str, key: str) -> bool:
    """Does provided tag match the tag embedded in the key

    Parameters
    ----------
    tag
        the tag to check. e.g., 'model' or 'antpos'
    key
        the key with an embedded tag. e.g., 'model:0382-38fd8-...'

    Returns
    -------
    bool
        True if tag matches, false otherwise

    """
    t = key.split(":")
    return len(t) == 2 and t[0] == tag


def get_all_data_for_user(userid, tag=None) -> list:
    keys = rdb.smembers(user_key(userid))

    # the user may have multiple entries, e.g., model:xyz, antpos:abc
    if tag is not None:
        return [x for x in keys if tag_match(tag, x)]


def get_antpos_json(antposid):
    if not antpos_exists(antposid):
        return None, None
    # request for a antpos. Note we can't use hmget because pickled data cannot automatically
    # be utf-8 decoded
    name = rdb.hget(antpos_key(antposid), KW_ANTPOSNAME)
    data = rpickle.hget(antpos_key(antposid), KW_DATA)

    if data:
        # recall that json payload is pickled into a string
        data = pickle.loads(data)
        return name, data
    else:
        return None, None
