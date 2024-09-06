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

    return render_template("receptionist/book_appointment.html", title="Book Appointment - Raseel")
