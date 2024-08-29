import models as m
from flask import render_template, redirect, url_for, request, flash, g
from flask_login import current_user, login_required
from urllib.parse import urlsplit
from web_flask import app, db, get_locale
from web_flask.forms import (
    EditProfileInfo,
    VisitorForm
)

import sqlalchemy as sa


@app.route("/", methods=["GET", "POST"])
def index():
    form = VisitorForm()
    if request.method == "POST":
        if form.validate_on_submit():
            flash("Your message has been sent!", "success")
    return render_template("index.html", title="Home - Raseel", form=form)




@app.route("/about")
def about():
    doctors = db.session.scalars(sa.select(m.Doctor))
    return render_template("about.html", title="About - Raseel", doctors=doctors)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = m.base_model.gen_datetime()
        db.session.commit()
    g.locale = str(get_locale())


@app.route("/edit_profile", methods=["GET", "POST"])
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
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.contact_number.data = current_user.contact_number
        form.address.data = current_user.address
        form.medical_history.data = current_user.medical_history
        form.current_medications.data = current_user.current_medications
        form.birth_date.data = current_user.birth_date
    return render_template("edit_profile.html", title="Edit Profile", form=form)

