from flask import Blueprint, render_template, request, g, current_app, session
from flask_login import current_user, login_required
from datetime import datetime, timedelta, timezone
import sqlalchemy as sa
import uuid

from web_flask import db
import models as m

doctor_bp = Blueprint("doctor_bp", __name__, url_prefix="/doctor")


def get_filtered_appointments(appointments):
    session["previous_endpoint"] = request.endpoint
    if g.search_form.validate():
        page = request.args.get("page", 1, type=int)
        search_results = m.Patient.search(
            g.search_form.q.data,
            page,
            current_app.config.get("SEARCH_RESULTS_PER_PAGE", 10),
        )
        apps = []
        for patient in search_results:
            for appointment in patient.appointments:
                if appointment.doctor_id == current_user.id:
                    apps.append(appointment)
        return [appointment for appointment in appointments if appointment in apps]
    return appointments


@doctor_bp.route("/appointments/current")
@login_required
def current_appointments():
    appointments = db.session.scalars(
        sa.select(m.Appointment).where(
            current_user.id == m.Appointment.doctor_id,
            sa.func.date(m.Appointment.appointment_time) == datetime.now().date(),
            m.Appointment.deleted_at == None,
        )
    )
    filtered_appointments = get_filtered_appointments(appointments)
    current_time_utc = datetime.now(timezone.utc)
    return render_template(
        "doctor/current.html",
        appointments=filtered_appointments,
        current_time_utc=current_time_utc,
        title="Current Appointments",
        cache_id=uuid.uuid4(),
    )


@doctor_bp.route("/appointments/upcoming")
@login_required
def upcoming_appointments():
    tomorrow = datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0
    ) + timedelta(days=1)
    appointments = db.session.scalars(
        sa.select(m.Appointment).where(
            current_user.id == m.Appointment.doctor_id,
            sa.func.date(m.Appointment.appointment_time) >= tomorrow,
            m.Appointment.deleted_at == None,
        )
    )
    filtered_appointments = get_filtered_appointments(appointments)
    current_time_utc = datetime.now(timezone.utc)
    return render_template(
        "doctor/upcoming.html",
        appointments=filtered_appointments,
        current_time_utc=current_time_utc,
        title="Upcoming Appointments",
        cache_id=uuid.uuid4(),
    )
