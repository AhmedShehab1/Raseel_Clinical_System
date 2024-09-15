from api.v1.errors import bad_request
from web_flask import db
from api.v1.views import bp, get_from_db
from models import Appointment, AppointmentStatus
from flask import request, flash
from datetime import datetime
import sqlalchemy as sa


def save(model=None):
    if model:
        db.session.add(model)
    db.session.commit()


def update_item(item, data):
    for k, v in data.items():
        if k in [
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
            "doctor_id",
            "patient_id",
        ]:
            continue
        setattr(item, k, v)
    save()


@bp.get("/appointments/<string:appointment_id>")
def get_appointment(appointment_id):
    app = get_from_db(appointment_id, Appointment)
    app.status = AppointmentStatus.CANCELLED
    return app.to_dict(), 200


@bp.delete("/appointments/<string:appointment_id>")
def delete_appointment(appointment_id):
    app = get_from_db(appointment_id, Appointment)

    app.deleted_at = datetime.utcnow()
    save()

    return {}, 200


@bp.post("/appointments")
def add_appointment():
    data = request.get_json()
    if (
        "patient_id" not in data
        or "doctor_id" not in data
        or "appointment_time" not in data
        or "status" not in data
    ):
        flash("Missing required fields", "danger")
        return bad_request("Missing required fields")

    if db.session.scalar(
        sa.select(Appointment).where(
            Appointment.appointment_time == data["appointment_time"],
            Appointment.doctor_id == data["doctor_id"],
        )
    ):
        flash("Doctor already has an appointment at that time", "danger")
        return bad_request("Doctor already has an appointment at that time")

    if db.session.scalar(
        sa.select(Appointment).where(
            Appointment.appointment_time == data["appointment_time"],
            Appointment.patient_id == data["patient_id"],
        )
    ):
        flash("Patient already has an appointment at that time", "danger")
        return bad_request("Patient already has an appointment at that time")

    app = Appointment(**data)
    save(app)
    flash("Appointment added successfully", "success")
    return app.to_dict(), 201


@bp.put("/appointments/<string:appointment_id>")
def update_app(appointment_id):
    app = get_from_db(appointment_id, Appointment)
    data = request.get_json()
    update_item(app, data)
    return app.to_dict(), 200
