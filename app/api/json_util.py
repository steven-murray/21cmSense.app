#
# json_util.py
#

from flask import jsonify


def json_error(errorcode, msg):
    """Return error in json format

    Parameters
    ----------
    errorcode
        errorcode (key)
    msg
        message (value)

    Returns
    -------
    Response
        k/v as json

    """
    return jsonify({errorcode: msg})

# def json_complex_error(errorcode, msg, **kwargs):
