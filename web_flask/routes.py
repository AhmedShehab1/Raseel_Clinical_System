from datetime import datetime, timezone
import models as m
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from urllib.parse import urlsplit
from web_flask import app, db
from web_flask.forms import LoginForm, RegistrationForm
import sqlalchemy as sa


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
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
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", title="Login - Raseel", form=form)


@app.route("/")
@login_required
def index():
    return render_template("index.html", title="Home - Raseel")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
    return render_template("about.html", title="About - Raseel")


@app.route('/user/<string:username>')
@login_required
def user(username):
    user = db.first_or_404(
        sa.select(m.Patient).where(m.Patient.name == username)
    )
    return render_template("user.html", user=user, title=f"{username} - Raseel")

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = m.base_model.gen_datetime()
        db.session.commit()