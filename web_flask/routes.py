import models as m
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from urllib.parse import urlsplit
from web_flask import app, db
from web_flask.email import send_password_reset_email
from web_flask.forms import LoginForm, RegistrationForm, EditProfileInfo, \
    ResetPasswordForm, ResetPasswordRequestForm
import sqlalchemy as sa


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('edit_profile'))
    form = LoginForm()
    if form.validate_on_submit():
        patient = db.session.scalar(
            sa.select(m.Patient).where(m.Patient.email == form.email.data)
        )
        if patient is None or not patient.check_password(form.password.data):
            flash('Login Unsuccessful. Please check email and password',
                  'danger')
            return redirect(url_for("login"))
        login_user(patient, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('edit_profile')
        return redirect(next_page)
    return render_template("login.html", title="Login - Raseel", form=form)


@app.route("/")
def index():
    return render_template("index.html", title="Home - Raseel")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('edit_profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        patient_data = {
            "name": form.name.data,
            "email": form.email.data,
            "contact_number": form.contact_number.data,
            "password": form.password.data
        }
        patient = m.Patient(**patient_data)
        db.session.add(patient)
        db.session.commit()
        flash('Your account has been created! You are now able to log in',
              'success')
        return redirect(url_for('login'))
    return render_template(
                           'register.html',
                           title='Register - Raseel',
                           form=form
                                    )


@app.route("/about")
def about():
    doctors = db.session.scalars(sa.select(m.Doctor))
    return render_template("about.html", title="About - Raseel", doctors=doctors)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = m.base_model.gen_datetime()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
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
        flash('Your changes have been saved', 'success')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.contact_number.data = current_user.contact_number
        form.address.data = current_user.address
        form.medical_history.data = current_user.medical_history
        form.current_medications.data = current_user.current_medications
        form.birth_date.data = current_user.birth_date
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('edit_profile'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        patient = db.session.scalar(
            sa.select(m.Patient).where(m.Patient.email == form.email.data)
        )
        if patient:
            send_password_reset_email(patient)
        flash(('An email has been sent with instructions to'
               ' reset your password'),
              'info')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password',
                           form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('edit_profile'))
    patient = m.Patient.verify_reset_password_token(token)
    if not patient:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        patient.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
