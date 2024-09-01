import models as m
from flask import Blueprint, render_template, request, flash
from web_flask import db
from web_flask.main.forms import (
    VisitorForm
)
import sqlalchemy as sa


receptionist_bp = Blueprint("receptionist_bp", __name__, url_prefix="/receptionist")

@receptionist_bp.route("/medical-departments")
def medical_departments():
    """
    A page to show the medical departments in the raseel medical center

    Returns:
        str: Render the receptionist template for veiwing the medical departments
    """

    return render_template("receptionist/medical_departments.html", title="Medical Departments - Raseel")

@receptionist_bp.route("/book-appointment")
def book_appointment():
    """
    Book an appointment for a patient

    Returns:
        str: Render the receptionist template for booking an appointiment
    """

    return render_template("receptionist/book_appointment.html", title="Book Appointment - Raseel")

@receptionist_bp.route("/about")
def about():
    """
    The about us page of the raseel center for the receptionist

    Returns:
        str: Render the receptionist template for view the about us page
    """

    doctors = db.session.scalars(sa.select(m.Doctor))
    return render_template("receptionist/about.html", title="About - Raseel", doctors=doctors)

@receptionist_bp.route("/", methods=["GET", "POST"])
def index():
    form = VisitorForm()
    if request.method == "POST":
        if form.validate_on_submit():
            flash("Your message has been sent!", "success")
    return render_template("receptionist/index.html", title="Home - Raseel", form=form)
