from flask import Blueprint, render_template, request
from flask_login import login_required
from web_flask.table_search import table_search
from datetime import datetime, timezone, timedelta

receptionist_bp = Blueprint("receptionist_bp", __name__, url_prefix="/receptionist")

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

    search_results = table_search()
    current_time_utc = datetime.utcnow
    tz = timedelta(hours=3)
    return render_template(
        'receptionist/dashboard.html',
        title='Receptionist Dashboard - Raseel',
        current_time_utc=current_time_utc,
        results=search_results,
        tz_delta=tz
    )
