import models as m
from web_flask import db
from flask import Blueprint, render_template
from flask_login import login_required
from web_flask.table_search import table_search
from datetime import datetime, timedelta
import sqlalchemy as sa

receptionist_bp = Blueprint("receptionist_bp", __name__, url_prefix="/receptionist")

def get_filtered_appointments_by_patients(appointments_list, patients_appointments):
    if patients_appointments and patients_appointments.keys().__len__() > 0:
        appointments_id = []
        for appointment in appointments_list:
            appointments_id.append(appointment.id)

        common_appointments_id = list(set(patients_appointments.keys()) & set(appointments_id))
        return [appointment for appointment in patients_appointments.values() if appointment.id in common_appointments_id]

    return appointments_list

@receptionist_bp.route("/book-appointment", methods=["GET", "POST"])
@login_required
def book_appointment():
    """Book an appointment for a patient

    Returns:
        str: Render the receptionist template for booking an appointiment
    """

    #Search on the patient
    search_results = table_search()

    return render_template("receptionist/book_appointment.html", title="Book Appointment - Raseel", patients=search_results)

@receptionist_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    """Dashboard page for the receptionist that shows the list of patients' appointments

    Returns:
        str: Render the receptionist dashboard template
    """
    nextWeek = datetime.utcnow().replace(
        hour=0, minute=0, second=0, microsecond=0
    ) + timedelta(days=7)

    patients_search = table_search()
    patients_appointments = {}
    if patients_search:
        for patient in patients_search:
            for appointment in patient.appointments:
                patients_appointments[appointment.id] = appointment
    else:
        patients_appointments = None

    today_appointments = db.session.scalars(
        sa.select(m.Appointment).where(
            sa.func.date(m.Appointment.appointment_time) == datetime.utcnow().date(),
            m.Appointment.deleted_at == None,
        )
    )
    today_appointments_filtered = get_filtered_appointments_by_patients(today_appointments.all(), patients_appointments)

    upcoming_appointments = db.session.scalars(
        sa.select(m.Appointment).where(
            sa.func.date(m.Appointment.appointment_time) > datetime.utcnow().date(),
            sa.func.date(m.Appointment.appointment_time) < nextWeek,
            m.Appointment.deleted_at == None,
        )
    )
    upcoming_appointments_filtered = get_filtered_appointments_by_patients(upcoming_appointments.all(), patients_appointments)

    current_time_utc = datetime.utcnow
    tz = timedelta(hours=3)

    return render_template(
        'receptionist/dashboard.html',
        title='Receptionist Dashboard - Raseel',
        current_time_utc=current_time_utc,
        patients=patients_search,
        today_appointments=today_appointments_filtered,
        upcoming_appointments=upcoming_appointments_filtered,
        tz_delta=tz
    )
