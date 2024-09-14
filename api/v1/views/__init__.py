# flake8: noqa
from flask import Blueprint, abort

bp = Blueprint("api", __name__, url_prefix="/api/v1")


def get_from_db(id, *models):
    for model in models:
        record = db.session.scalar(
            sa.select(model).where(model.id == id, model.deleted_at == None)
        )
        if record:
            return record
    abort(404)


from api.v1.views.appointments import *
from api.v1.views.departments import *
from api.v1.errors import *
from api.v1.views.patients import *
from api.v1.views.members import *
from api.v1.views.email import *
