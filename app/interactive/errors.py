from flask import render_template
from . import interactive


@interactive.app_errorhandler(500)
def internal_server_error_500(err):
    return render_template('500.html'), 500
