from flask import Blueprint

bp = Blueprint("main", __name__)

from web_flask.main import routes
