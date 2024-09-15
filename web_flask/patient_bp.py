from flask import Blueprint, render_template
from flask_login import current_user, login_required
from web_flask.table_search import table_search
from datetime import datetime, timezone


patient_bp = Blueprint("patient_bp", __name__, url_prefix="/patient")


@patient_bp.route("/book-appointment", methods=["GET", "POST"])
@login_required
def patient_book_appointment():
    """
    Book an appointment for a patient using his/her account

    Returns:
        str: Render the patient template for booking an appointiment
    """

    # Search on the patient
    search_results = table_search()

    return render_template(
        "patient/book_appointment.html",
        title="Book Appointment - Raseel",
        patients=search_results,
        current_user=current_user,
    )


@patient_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    """Dashboard page for the patient that shows the list of their appointments

    Returns:
        str: Render the patient dashboard template
    """

    current_time_utc = datetime.now(timezone.utc)
    return render_template(
        "patient/dashboard.html",
        title="Dashboard - Raseel",
        current_time_utc=current_time_utc,
        appointments=current_user.appointments,
    )
