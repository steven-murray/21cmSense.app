#
# errors.py
#

from flask import render_template
from . import api
from flask import jsonify


@api.errorhandler(418)
def not_found_418(err):
    return render_template('418.html'), 404


