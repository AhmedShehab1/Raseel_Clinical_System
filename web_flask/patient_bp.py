from flask import Blueprint, render_template


patient_bp = Blueprint("patient_bp", __name__, url_prefix="/patient")

@patient_bp.route("/medical-departments")
def medical_departments():
    """
    A page to show the medical departments in the raseel medical center

    Returns:
        str: Render the patient template for veiwing the medical departments
    """

    return render_template("patient/medical_departments.html", title="Medical Departments")

@patient_bp.route("/book-appointment")
def patient_book_appointment():
    """
    Book an appointment for a patient using his/her account

    Returns:
        str: Render the patient template for booking an appointiment
    """

    return render_template("patient/book_appointment.html", title="Book Appointment")
