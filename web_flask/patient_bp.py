import models as m
from flask import Blueprint, render_template, request, flash
from web_flask import db
from web_flask.main.forms import (
    VisitorForm
)
import sqlalchemy as sa


patient_bp = Blueprint("patient_bp", __name__, url_prefix="/patient")

@patient_bp.route("/medical-departments")
def medical_departments():
    """
    A page to show the medical departments in the raseel medical center

    Returns:
        str: Render the patient template for veiwing the medical departments
    """

    return render_template("patient/medical_departments.html", title="Medical Departments - Raseel")

@patient_bp.route("/book-appointment")
def patient_book_appointment():
    """
    Book an appointment for a patient using his/her account

    Returns:
        str: Render the patient template for booking an appointiment
    """

    return render_template("patient/book_appointment.html", title="Book Appointment")

@patient_bp.route("/about")
def about():
    """
    The about us page of the raseel center for the patient

    Returns:
        str: Render the patient template for view the about us page
    """

    doctors = db.session.scalars(sa.select(m.Doctor))
    return render_template("patient/about.html", title="About - Raseel", doctors=doctors)

@patient_bp.route("/", methods=["GET", "POST"])
def index():
    form = VisitorForm()
    if request.method == "POST":
        if form.validate_on_submit():
            flash("Your message has been sent!", "success")
    return render_template("patient/index.html", title="Home - Raseel", form=form)
