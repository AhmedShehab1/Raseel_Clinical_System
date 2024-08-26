from flask import Blueprint, render_template

doctor_bp = Blueprint('doctor_bp', __name__, url_prefix='/doctor')


@doctor_bp.route('/appointments/current')
def current_appointments():
    return render_template('doctor/current.html',
                           title='Current Appointments')


@doctor_bp.route('/appointments/upcoming')
def upcoming_appointments():
    return render_template('doctor/upcoming.html',
                           title='Upcoming Appointments')
