from urllib.parse import urlsplit
from web_flask.auth import bp
from web_flask import db
from flask import redirect, url_for, render_template, flash, request
from flask_login import logout_user, current_user, login_user
from web_flask.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm
from web_flask.auth.email import send_password_reset_email
import sqlalchemy as sa
import models as m


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("receptionist_bp.edit_profile"))
    form = LoginForm()
    if form.validate_on_submit():
        patient = db.session.scalar(
            sa.select(m.Patient).where(m.Patient.email == form.email.data)
        )
        if patient is None or not patient.check_password(form.password.data):
            flash("Login Unsuccessful. Please check email and password",
                  "danger")
            return redirect(url_for("auth.login"))
        login_user(patient, remember=form.remember.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("receptionist_bp.edit_profile")
        return redirect(next_page)
    return render_template("login.html", title="Login - Raseel", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("receptionist_bp.edit_profile"))
    form = RegistrationForm()
    if form.validate_on_submit():
        patient_data = {
            "name": form.name.data,
            "email": form.email.data,
            "contact_number": form.contact_number.data,
            "password": form.password.data,
            "birth_date": form.birth_date.data,
        }
        patient = m.Patient(**patient_data)
        db.session.add(patient)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", title="Register - Raseel", form=form)



@bp.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("receptionist_bp.edit_profile"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        patient = db.session.scalar(
            sa.select(m.Patient).where(m.Patient.email == form.email.data)
        )
        if patient:
            send_password_reset_email(patient)
        flash(
            ("An email has been sent with instructions to"
             " reset your password"),
            "info",
        )
        return redirect(url_for("auth.login"))
    return render_template("reset_password.html", title="Reset Password", heading="Reset Password", form=form)


@bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("receptionist_bp.edit_profile"))
    patient = m.Patient.verify_reset_password_token(token)
    if not patient:
        return redirect(url_for("main.index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        patient.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset.", "success")
        return redirect(url_for("auth.login"))
    return render_template("reset_password.html", title="Reset Password", heading="Reset Password", form=form)
