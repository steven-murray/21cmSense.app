# from flask import Blueprint
from flask import Flask, request, render_template
from flask_cors import CORS

# mod_main = Blueprint('mod_main', __name__)
# from app.mod_main import main as main_blueprint
# app.register_blueprint(main_blueprint)

# from . import views, errors

def register_errorhandlers(app):
    @app.errorhandler(404)
    def _handle_api_error(ex):
        if request.path.startswith('/api'):
            return render_template('json_404.html'), 404
        else:
            return render_template('404.html'), 404


def create_app(config_name):
    from .api import api as api_blueprint
    from .interactive import interactive as interactive_blueprint

    app = Flask(__name__)
    CORS(app)
    register_errorhandlers(app)

    app.register_blueprint(api_blueprint, url_prefix='/api-1.0')
    app.register_blueprint(interactive_blueprint, url_prefix='/')
    return app
