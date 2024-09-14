import models as m
from flask import render_template, redirect, url_for, request, flash, g
from flask_login import current_user, login_required
from web_flask.main import bp
from web_flask import db, get_locale, login_manager
from web_flask.main.forms import EditProfileInfo, VisitorForm, SearchForm

import sqlalchemy as sa


@bp.route("/medical-departments")
def medical_departments():
    return render_template(
        "medical_departments.html", title="Medical Departments - Raseel"
    )


@bp.route("/", methods=["GET", "POST"])
def index():
    form = VisitorForm()
    if request.method == "POST":
        if form.validate_on_submit():
            flash("Your message has been sent!", "success")
    return render_template("index.html", title="Home - Raseel", form=form)


@bp.route("/about")
def about():
    doctors = db.session.scalars(sa.select(m.Doctor))
    return render_template("about.html", title="About - Raseel", doctors=doctors)


@bp.before_app_request
def before_request():
    if (
        request.endpoint == "auth.staff_login"
    ):  # This should be changed to ['staff.raseel.com'] in request.host
        login_manager.login_view = "auth.staff_login"
        login_manager.login_message = "Staff: Please log in to access this page."
    else:
        login_manager.login_view = "auth.login"
        login_manager.login_message = "Please log in to access this page."

    if current_user.is_authenticated:
        current_user.last_seen = m.base_model.gen_datetime()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route("/edit_profile", methods=["GET", "POST"])
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
        return redirect(url_for("main.edit_profile"))
    elif request.method == "GET":
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.contact_number.data = current_user.contact_number
        form.address.data = current_user.address
        form.medical_history.data = current_user.medical_history
        form.current_medications.data = current_user.current_medications
        form.birth_date.data = current_user.birth_date
    return render_template("edit_profile.html", title="Edit Profile", form=form)
