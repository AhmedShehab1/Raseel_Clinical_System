from models.base_model import BaseModel
from models.doctor import Doctor
from models.patient import Patient
import sqlalchemy as sa
import sqlalchemy.orm as so
from enum import Enum


class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Appointment(BaseModel):
    """
    Appointment model class
    """

    __tablename__ = "appointments"
    patient_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("patients.id"), index=True
    )
    doctor_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("doctors.id"), index=True
    )
    appointment_time: so.Mapped[sa.DateTime] = so.mapped_column(
        sa.DateTime, index=True, nullable=False
    )
    status: so.Mapped[AppointmentStatus] = so.mapped_column(
        sa.Enum(AppointmentStatus), index=True, nullable=False
    )
    reason: so.Mapped[str] = so.mapped_column(sa.String(256))
    notes: so.Mapped[str] = so.mapped_column(sa.String(256))
    patient: so.Mapped["Patient"] = so.relationship(
        "Patient", back_populates="appointments"
    )
    doctor: so.Mapped["Doctor"] = so.relationship(
        "Doctor", back_populates="appointments"
    )
