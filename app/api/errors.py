#
# errors.py
#
# Project 43 - Web Application for Radio Astronomy Sensitivity
# Author: Brian Pape
# Revision: 0.1
#
# This module contains a flask error handler for 418 not found errors

from flask import render_template
from . import api
from flask import jsonify


@api.errorhandler(418)
def not_found_418(err):
    return render_template('418.html'), 404


