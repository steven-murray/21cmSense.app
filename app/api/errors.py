from flask import render_template
from . import api


@api.errorhandler(418)
def not_found_418(err):
    return render_template('418.html'), 404

