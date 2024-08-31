from flask import Blueprint, render_template


receptionist_bp = Blueprint("receptionist_bp", __name__, url_prefix="/receptionist")

@receptionist_bp.route("/book-appointment")
def book_appointment():
    """
    Book an appointment for a patient

    Returns:
        str: Render the reciptionist template for booking an appointiment
    """

    return render_template("receptionist/book_appointment.html", title="Book Appointment")
