from api.v1.errors import bad_request
from web_flask import db
from api.v1.views import bp,  get_from_db
from models import Appointment, AppointmentStatus
from flask import request, flash, abort
from datetime import datetime, timezone
import sqlalchemy as sa


def appointment_available(doctor_id, patient_id, appointment_time):
    if db.session.scalar(sa.select(Appointment).where(
        Appointment.appointment_time == appointment_time,
        Appointment.doctor_id == doctor_id,
        Appointment.status == AppointmentStatus.SCHEDULED
        )):
        flash('Doctor already has an appointment at that time', 'danger')
        return False

    if db.session.scalar(sa.select(Appointment).where(
        Appointment.appointment_time == appointment_time,
        Appointment.patient_id == patient_id,
        Appointment.status == AppointmentStatus.SCHEDULED
        )):
        flash('Patient already has an appointment at that time', 'danger')
        return False
    return True

def get_app_from_db(id, *models):
    for model in models:
        record = db.session.scalar(sa.select(model).where(
            model.id == id,
            ))
        if record:
            return record
    abort(404)

def save(model=None):
    if model:
        db.session.add(model)
    db.session.commit()


def update_item(item, data):
    for k, v in data.items():
        if k in ['id', 'created_at', 'updated_at', 'deleted_at','doctor_id', 'patient_id']:
            continue
        setattr(item, k, v)
    save()

@bp.get('/appointments/<string:appointment_id>')
def get_appointment(appointment_id):
    app = get_from_db(appointment_id, Appointment)
    return app.to_dict(), 200


@bp.delete('/appointments/<string:appointment_id>')
def delete_appointment(appointment_id):
    app = get_from_db(appointment_id, Appointment)

    app.deleted_at = datetime.utcnow()
    app.status = AppointmentStatus.CANCELLED
    save()
    flash('Appointment deleted successfully', 'success')
    return {}, 200


@bp.post('/appointments')
def add_appointment():
    data = request.get_json()
    if 'patient_id' not in data or 'doctor_id' not in data or 'appointment_time' not in data or 'status' not in data:
        flash('Missing required fields', 'danger')
        return bad_request('Missing required fields')

    if not appointment_available(data['doctor_id'], data['patient_id'], data['appointment_time']):
        return {}, 400

    app = Appointment(**data)
    save(app)
    flash('Appointment added successfully', 'success')
    return app.to_dict(), 201

@bp.put('/appointments/<string:appointment_id>')
def update_app(appointment_id):
    app = get_from_db(appointment_id, Appointment)
    data = request.get_json()
    update_item(app, data)
    flash('Appointment updated successfully', 'success')
    return app.to_dict(), 200

@bp.put('/appointments/2/<string:appointment_id>')
def restore_app(appointment_id):
    app = get_app_from_db(appointment_id, Appointment)

    if app.appointment_time < datetime.utcnow():
        flash('Cannot restore past appointments', 'danger')
        return {}, 400

    if not appointment_available(app.doctor_id, app.patient_id, app.appointment_time):
        return {}, 400

    app.deleted_at = None
    app.status = AppointmentStatus.SCHEDULED
    flash('Appointment restored successfully', 'success')
    save()
    return app.to_dict(), 200
