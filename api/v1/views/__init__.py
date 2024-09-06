# flake8: noqa
from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api/v1')

from api.v1.views.appointments import *
from api.v1.views.departments import *
from api.v1.errors import *
from api.v1.views.patients import *
