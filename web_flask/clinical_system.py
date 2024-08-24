# flake8: noqa
from web_flask import app, db
from models.base_model import BaseModel
import models as m

@app.shell_context_processor
def make_shell_context():
    return {
        "app": app,
        "db": db,
        "BaseModel": BaseModel,
        "Patient": m.Patient,
        "Doctor": m.Doctor,
        "Appointment": m.Appointment,
        "Department": m.Department,
        "TimeSlot": m.TimeSlot
    }
