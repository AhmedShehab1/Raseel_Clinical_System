import models as m
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from web_flask import db
from web_flask.main.forms import (
    EditProfileInfo,
    VisitorForm
)
import sqlalchemy as sa


receptionist_bp = Blueprint("receptionist_bp", __name__, url_prefix="/receptionist")

@receptionist_bp.route("/book-appointment", methods=["GET", "POST"])
@login_required
def book_appointment():
    """Book an appointment for a patient

    Returns:
        str: Render the receptionist template for booking an appointiment
    """
    if request.method == "POST":
        """Add the appointment to the database"""
        pass

    return render_template("receptionist/book_appointment.html", title="Book Appointment - Raseel")

@receptionist_bp.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileInfo(current_user.email, current_user.contact_number)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.contact_number = form.contact_number.data
        current_user.address = form.address.data
        current_user.medical_history = form.medical_history.data
        current_user.current_medications = form.current_medications.data
        current_user.birth_date = form.birth_date.data
        db.session.commit()
        flash("Your changes have been saved", "success")
        return redirect(url_for("receptionist_bp.edit_profile"))
    elif request.method == "GET":
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.contact_number.data = current_user.contact_number
        form.address.data = current_user.address
        form.medical_history.data = current_user.medical_history
        form.current_medications.data = current_user.current_medications
        form.birth_date.data = current_user.birth_date
    return render_template("receptionist/edit_profile.html", title="Edit Profile", form=form)
