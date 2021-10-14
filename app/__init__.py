# from flask import Blueprint
from flask import Flask, render_template


# mod_main = Blueprint('mod_main', __name__)
# from app.mod_main import main as main_blueprint
# app.register_blueprint(main_blueprint)

# from . import views, errors

def create_app(config_name):
    from .api import api as api_blueprint
    from .interactive import interactive as interactive_blueprint

    app = Flask(__name__)
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(interactive_blueprint, url_prefix='/')
    return app

