from web_flask import db
from api.v1.views import bp
from models import Appointment
from flask import request
from datetime import datetime

def get_app(app_id):
    return db.get_or_404(Appointment, app_id)

def save():
    db.session.commit()

def update_item(item, data):
    for k, v in data.items():
        if k in ['id', 'created_at', 'updated_at', 'deleted_at','doctor_id', 'patient_id']:
            continue
        setattr(item, k, v)
    save()

@bp.get('/appointments/<string:appointment_id>')
def get_appointment(appointment_id):
    app = get_app(appointment_id)
    return app.to_dict(), 200


@bp.delete('/appointments/<string:appointment_id>')
def delete_appointment(appointment_id):
    app = get_app(appointment_id)

    app.deleted_at = datetime.utcnow()
    save()

    return {}, 200


@bp.put('/appointments/<string:appointment_id>')
def update_app(appointment_id):
    app = get_app(appointment_id)
    data = request.get_json()
    update_item(app, data)
    return app.to_dict(), 200
