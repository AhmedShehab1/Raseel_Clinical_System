# flake8: noqa
from web_flask import db, create_app
from models.base_model import BaseModel
import models as m
import sqlalchemy as sa
import sqlalchemy.orm as so

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "BaseModel": BaseModel,
        "Patient": m.Patient,
        "Doctor": m.Doctor,
        "Appointment": m.Appointment,
        "Department": m.Department,
        "TimeSlot": m.TimeSlot,
        "WorkingHours": m.WorkingHours,
        "AppointmentStatus": m.AppointmentStatus,
        "Admin": m.Admin,
        "StaffMember": m.StaffMember,
        "sa": sa,
        "so": so,
    }
