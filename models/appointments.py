from typing import Optional
from .base_model import BaseModel
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
    reason: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    patient: so.Mapped["m.Patient"] = so.relationship(
        "Patient", back_populates="appointments"
    )
    doctor: so.Mapped["m.Doctor"] = so.relationship(
        "Doctor", back_populates="appointments"
    )
