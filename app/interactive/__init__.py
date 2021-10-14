from flask import Blueprint

interactive = Blueprint('interactive', __name__)

from . import views, errors

