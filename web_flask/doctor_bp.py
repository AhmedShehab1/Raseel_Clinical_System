from flask import Blueprint, render_template
from web_flask import db
import sqlalchemy as sa
import models as m
from flask_login import current_user

doctor_bp = Blueprint("doctor_bp", __name__, url_prefix="/doctor")


@doctor_bp.route("/appointments/current")
def current_appointments():
    appointments = db.session.scalars(
        sa.select(m.Appointment).where(current_user.id == m.Appointment.patient_id)
    )
    return render_template(
        "doctor/current.html", appointments=appointments, title="Current Appointments"
    )


@doctor_bp.route("/appointments/upcoming")
def upcoming_appointments():
    return render_template("doctor/upcoming.html", title="Upcoming Appointments")


@doctor_bp.route("/appointments/update/<string:appointment_id>")
def update_appointment(appointment_id):
    pass


@doctor_bp.route("/appointments/delete/<string:appointment_id>")
def delete_appointment(appointment_id):
    pass


@doctor_bp.route("/appointments/view/<string:appointment_id>")
def view_appointment(appointment_id):
    pass
