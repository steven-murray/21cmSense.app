#
# errors.py
#

from flask import render_template
from . import interactive


# provide a rendered
@interactive.app_errorhandler(500)
def internal_server_error_500(err):
    """Provided a templated 500 server error
    """
    return render_template('500.html'), 500
