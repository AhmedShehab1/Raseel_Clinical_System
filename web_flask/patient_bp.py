from flask import Blueprint, render_template, redirect, url_for, request, flash
from web_flask import db
from flask_login import current_user, login_required
from web_flask.main.forms import (
    EditProfileInfo,
)


patient_bp = Blueprint("patient_bp", __name__, url_prefix="/patient")

@patient_bp.route("/book-appointment")
@login_required
def patient_book_appointment():
    """
    Book an appointment for a patient using his/her account

    Returns:
        str: Render the patient template for booking an appointiment
    """

    return render_template("patient/book_appointment.html", title="Book Appointment - Raseel")

@patient_bp.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    """
    Edit the profile of a patient using his/her account

    Returns:
        str: Render the patient edit profile template
    """

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
        return redirect(url_for("patient_bp.edit_profile"))
    elif request.method == "GET":
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.contact_number.data = current_user.contact_number
        form.address.data = current_user.address
        form.medical_history.data = current_user.medical_history
        form.current_medications.data = current_user.current_medications
        form.birth_date.data = current_user.birth_date
    return render_template("patient/edit_profile.html", title="Edit Profile", form=form)
