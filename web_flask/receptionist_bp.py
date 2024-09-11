import models as m
from flask import Blueprint, render_template, request, session, g, current_app
from flask_login import login_required


receptionist_bp = Blueprint("receptionist_bp", __name__, url_prefix="/receptionist")

def search_patients():
    session['previous_endpoint'] = request.endpoint
    if g.search_form.validate():
        page = request.args.get("page", 1, type=int)
        search_results, _ = m.Patient.search(g.search_form.q.data, page,
                                                current_app.config.get('SEARCH_RESULTS_PER_PAGE', 10))
        return search_results
    return None

@receptionist_bp.route("/book-appointment", methods=["GET", "POST"])
@login_required
def book_appointment():
    """Book an appointment for a patient

    Returns:
        str: Render the receptionist template for booking an appointiment
    """

    if request.method == "GET":
        #Search on the patient
        search_results = search_patients()

    return render_template("receptionist/book_appointment.html", title="Book Appointment - Raseel", patients=search_results)

@receptionist_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    """Dashboard page for the receptionist that shows the list of patients' appointments

    Returns:
        str: Render the receptionist dashboard template
    """

    return render_template("receptionist/dashboard.html", title="Receptionist Dashboard - Raseel")
