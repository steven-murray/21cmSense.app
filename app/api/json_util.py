#
# json_util.py
#
# Project 43 - Web Application for Radio Astronomy Sensitivity
# Author: Brian Pape
# Revision: 0.1
#
# This module contains json utilities

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
