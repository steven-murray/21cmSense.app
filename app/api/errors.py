from flask import render_template
from .__init__ import api


@api.app_errorhandler(404)
def not_found_404(err):
    return render_template('404.html'), 404


@api.app_errorhandler(500)
def internal_server_error_500(err):
    return render_template('500.html'), 500
