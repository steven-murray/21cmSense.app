# from flask import Blueprint
from flask import Flask, render_template, request
from flask_cors import CORS


def register_errorhandlers(app):
    @app.errorhandler(404)
    def _handle_api_error(ex):
        if request.path.startswith("/api-1.0"):
            return render_template("json_404.html"), 404
        else:
            return render_template("404.html"), 404


def create_app():
    from .api import api as api_blueprint

    app = Flask(__name__)
    CORS(app)
    register_errorhandlers(app)

    app.register_blueprint(api_blueprint, url_prefix="/api-1.0")
    return app
