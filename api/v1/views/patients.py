from datetime import datetime
from api.v1.errors import bad_request
from api.v1.views import bp, get_from_db
from web_flask import db
from models import Patient
from models import Prescription
from models import Diagnose
import sqlalchemy as sa
from flask import request, flash
from api.v1.views.departments import listAllObjects as AllPatients
from sqlalchemy.orm import joinedload


def save(model=None):
    if model:
        db.session.add(model)
    db.session.commit()
    print(model)  # DONOT DELETE IT, To show the ID of the model saved


def update_data(model, data):
    if (
        "email" in data
        and data["email"] != model.email
        and db.session.scalar(sa.select(Patient).where(Patient.email == data["email"]))
    ):
        return bad_request("Email already exists")
    if (
        "contact_number" in data
        and data["contact_number"] != model.contact_number
        and db.session.scalar(
            sa.select(Patient).where(Patient.contact_number == data["contact_number"])
        )
    ):
        return bad_request("Contact number already exists")
    if (
        "national_id" in data
        and data["national_id"] != model.national_id
        and db.session.scalar(
            sa.select(Patient).where(Patient.national_id == data["national_id"])
        )
    ):
        return bad_request("National ID already exists")
    for k, v in data.items():
        if k in [
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
            "last_seen",
            "password_hash",
        ]:
            continue
        setattr(model, k, v)
    save()


@bp.get("/patients/<string:patient_id>")
def get_patient(patient_id):
    return get_from_db(patient_id, Patient).to_dict(), 200


@bp.delete("/patients/<string:patient_id>")
def delete_patient(patient_id):
    patient = get_from_db(patient_id, Patient)

    patient.deleted_at = datetime.utcnow()
    save()

    return {}, 200


@bp.post("/patients")
def add_patient():
    data = request.get_json()
    if (
        "name" not in data
        or "email" not in data
        or "contact_number" not in data
        or "birth_date" not in data
        or "password" not in data
        or "national_id" not in data
        or "gender" not in data
    ):
        flash("Missing required fields", "danger")
        return bad_request("Missing required fields")
    if db.session.scalar(sa.select(Patient).where(Patient.email == data["email"])):
        flash("Email already exists", "danger")
        return bad_request("Email already exists")
    if db.session.scalar(
        sa.select(Patient).where(Patient.contact_number == data["contact_number"])
    ):
        flash("Contact number already exists", "danger")
        return bad_request("Contact number already exists")
    if db.session.scalar(
        sa.select(Patient).where(Patient.national_id == data["national_id"])
    ):
        flash("National ID already exists", "danger")
        return bad_request("National ID already exists")
    patient = Patient(**data)
    save(patient)
    flash("Account added successfully", "success")
    return patient.to_dict(), 201


@bp.put("/patients/<string:patient_id>")
def update_patient(patient_id):
    patient = get_from_db(patient_id, Patient)
    data = request.get_json()
    update_data(patient, data)
    return patient.to_dict(), 200


@bp.post("/patients/<string:patient_id>/medications")
def add_medication(patient_id):
    _ = get_from_db(patient_id, Patient)
    data = request.get_json()
    if "medication" not in data or "dosage" not in data:
        bad_request("Missing required fields")
    prescription = Prescription(
        patient_id=patient_id, medication=data["medication"], dosage=data["dosage"]
    )
    save(prescription)
    return {"message": "Medication added successfully"}, 201


@bp.post("/patients/<string:patient_id>/diagnosises")
def add_diagnosis(patient_id):
    _ = get_from_db(patient_id, Patient)
    data = request.get_json()
    if "name" not in data:
        bad_request("Missing required fields")
    diagnosis = Diagnose(patient_id=patient_id, name=data["name"])
    save(model=diagnosis)
    return {"message": "Diagnosis added successfully"}, 201


@bp.get("/patients")
def get_all_patients():
    """Get all patients in the database.

    Returns:
        dict: a json format containing the count of patients and a list of
            dictionaries representing each department.
        int: the status code of the response.
    """

    patients_list = (
        db.session.query(Patient).options(joinedload(Patient.appointments)).all()
    )
    patients = AllPatients(patients_list)
    if patients.count > 0:
        status_code = 200
    else:
        status_code = 404
        return bad_request(
            "Failed to load the accounts of patients, please try again later"
        )

    return patients.to_dict(), status_code
