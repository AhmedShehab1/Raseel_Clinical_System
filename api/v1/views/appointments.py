from api.v1.errors import bad_request
from web_flask import db
from api.v1.views import bp
from models import Appointment
from flask import request
from datetime import datetime
import sqlalchemy as sa

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

# Get all appointments of a specific doctor
@bp.get('/appointments/<string:doctor_id>')
def get_doctor_appointments(doctor_id):
    appointments = db.session.scalars(sa.select(Appointment).where(Appointment.doctor_id == doctor_id)).all()
    return [app.to_dict() for app in appointments], 200

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


@bp.post('/appointments')
def add_appointment():
    data = request.get_json()
    if 'patient_id' not in data or 'doctor_id' not in data or 'appointment_time' not in data or 'status' not in data:
        return bad_request('Missing required fields')

    if db.session.scalar(sa.select(Appointment).where(
        Appointment.appointment_time == data['appointment_time'],
        Appointment.doctor_id == data['doctor_id']
        )):
        return bad_request('Doctor already has an appointment at that time')

    if db.session.scalar(sa.select(Appointment).where(
        Appointment.appointment_time == data['appointment_time'],
        Appointment.patient_id == data['patient_id']
        )):
        return bad_request('Patient already has an appointment at that time')

    app = Appointment(**data)
    db.session.add(app)
    save()
    return app.to_dict(), 201

@bp.put('/appointments/<string:appointment_id>')
def update_app(appointment_id):
    app = get_app(appointment_id)
    data = request.get_json()
    update_item(app, data)
    return app.to_dict(), 200
