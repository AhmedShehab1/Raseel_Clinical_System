from flask import Blueprint, render_template, request
from flask_login import login_required
from web_flask.search_patients import search_patients

receptionist_bp = Blueprint("receptionist_bp", __name__, url_prefix="/receptionist")

@receptionist_bp.route("/book-appointment", methods=["GET", "POST"])
@login_required
def book_appointment():
    """Book an appointment for a patient

    Returns:
        str: Render the receptionist template for booking an appointiment
    """

    #Search on the patient
    search_results = search_patients()

    return render_template("receptionist/book_appointment.html", title="Book Appointment - Raseel", patients=search_results)

@receptionist_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    """Dashboard page for the receptionist that shows the list of patients' appointments

    Returns:
        str: Render the receptionist dashboard template
    """

    return render_template("receptionist/dashboard.html", title="Receptionist Dashboard - Raseel")
