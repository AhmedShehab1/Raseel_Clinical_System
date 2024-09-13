from urllib.parse import urlsplit
from web_flask.auth import bp
from web_flask import db
from flask import (
    redirect,
    url_for,
    render_template,
    flash,
    request,
    session,abort
    )
from flask_login import logout_user, current_user, login_user
from web_flask.auth.forms import (
    LoginForm,
    RegistrationForm,
    ResetPasswordForm,
    ResetPasswordRequestForm
    )
from web_flask.auth.email import send_password_reset_email
from functools import wraps
import sqlalchemy as sa
import models as m

ROLE_DASHBOARD_MAP = {
    'Admin': 'admin_bp.admin_dashboard',
    'Doctor': 'doctor_bp.current_appointments',
    'Receptionist': 'receptionist_bp.dashboard',
}


def get_staff_by_email(email: str):
    result = m.StaffMember.search(email, 1, 1, ['email'])
    if result and result[0].deleted_at is None:
        return result[0]
    return None

def login_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        form = args[0]
        staff = get_staff_by_email(form.email.data)
        print(staff)
        if staff is None or not staff.check_password(form.password.data):
            flash("Login Unsuccessful. Please check email and password",
                  "danger")
            return redirect(url_for('auth.staff_login'))
        login_user(staff, remember=form.remember.data)
        session['user_type'] = staff.__class__.__name__

        return func(*args, staff=staff, **kwargs)

    return wrapper


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.host == 'staff.ahmedshehab.tech':
        return redirect(url_for('auth.staff_login'))
    if current_user.is_authenticated:
        return redirect(url_for("patient_bp.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        patient = db.session.scalar(
            sa.select(m.Patient).where(m.Patient.email == form.email.data)
        )
        if patient is None or not patient.check_password(form.password.data):

            return redirect(url_for("auth.login"))
        login_user(patient, remember=form.remember.data)
        session['user_type'] = patient.__class__.__name__
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("patient_bp.dashboard")
        return redirect(next_page)
    return render_template("login.html", title="Login - Raseel", form=form)


@bp.route("/staff/login", methods=["GET", "POST"])
def staff_login():
    if current_user.is_authenticated:
        return redirect(url_for(ROLE_DASHBOARD_MAP[session['user_type']]))

    form = LoginForm()
    if form.validate_on_submit():
        process_login(form)

    return render_template("login.html", title="Staff Login - Raseel", form=form)

@login_handler
def process_login(form, staff):
    next_page = request.args.get("next")
    dashboard_route = ROLE_DASHBOARD_MAP.get(session['user_type'])
    if not dashboard_route:
         flash("Role does not have an assigned dashboard.", "warning")
         return redirect(url_for("auth.staff_login"))
    if not next_page or urlsplit(next_page).netloc != "":
        next_page = url_for(dashboard_route)
    return redirect(next_page)

@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("patient_bp.dashboard"))
    form = RegistrationForm()
    if form.validate_on_submit():
        patient_data = {
            "name": form.name.data,
            "email": form.email.data,
            "contact_number": form.contact_number.data,
            "password": form.password.data,
            "birth_date": form.birth_date.data,
            "gender": m.GenderType(form.gender.data),
            "national_id": form.national_id.data
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
        return redirect(url_for("patient_bp.dashboard"))
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
        return redirect(url_for("patietn_bp.dashboard"))
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
