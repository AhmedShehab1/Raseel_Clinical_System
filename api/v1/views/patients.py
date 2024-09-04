from datetime import datetime
from api.v1.errors import bad_request
from api.v1.views import bp
from web_flask import db
from models import Patient
import sqlalchemy as sa
from flask import request

def get_patient(patient_id):
    return db.get_or_404(Patient, patient_id)

def save():
    db.session.commit()

def update_patient(patient, data):
    if 'email' in data and data['email'] != patient.email and db.session.scalar(sa.select(Patient).where(Patient.email == data['email'])):
        return bad_request('Email already exists')
    if 'contact_number' in data and data['contact_number'] != patient.contact_number and db.session.scalar(sa.select(Patient).where(Patient.contact_number == data['contact_number'])):
        return bad_request('Contact number already exists')
    if 'national_id' in data and data['national_id'] != patient.national_id and db.session.scalar(sa.select(Patient).where(Patient.national_id == data['national_id'])):
        return bad_request('National ID already exists')
    for k, v in data.items():
        if k in ['id', 'created_at', 'updated_at', 'deleted_at', 'last_seen', 'password_hash']:
            continue
        setattr(patient, k, v)
    save()


@bp.get('/patients/<string:patient_id>')
def get_patient(patient_id):
    return get_patient(patient_id).to_dict(), 200


@bp.delete('/patients/<string:patient_id>')
def delete_patient(patient_id):
    patient = get_patient(patient_id)

    patient.deleted_at = datetime.utcnow()
    save()

    return {}, 200

@bp.post('/patients')
def add_patient():
    data = request.get_json()
    if 'name' not in data or 'email' not in data or 'contact_number' not in data or 'birth_date' not in data or 'password' not in data or 'national_id' not in data or 'gender' not in data:
        return bad_request('Missing required fields')
    if db.session.scalar(sa.select(Patient).where(Patient.email == data['email'])):
        return bad_request('Email already exists')
    if db.session.scalar(sa.select(Patient).where(Patient.contact_number == data['contact_number'])):
        return bad_request('Contact number already exists')
    if db.session.scalar(sa.select(Patient).where(Patient.national_id == data['national_id'])):
        return bad_request('National ID already exists')
    patient = Patient(**data)
    db.session.add(patient)
    save()
    return patient.to_dict(), 201

@bp.put('/patients/<string:patient_id>')
def update_patient(patient_id):
    patient = get_patient(patient_id)
    data = request.get_json()
    update_patient(patient, data)
    return patient.to_dict(), 200
