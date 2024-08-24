from typing import List, Optional
from models.appointments import Appointment
from models.base_model import BaseModel
from models.department import Department
from models.timeslot import TimeSlot
import sqlalchemy as sa
import sqlalchemy.orm as so
from utils import PasswordMixin


class Doctor(BaseModel, PasswordMixin):
    """
    Doctor model class
    Args:
        BaseModel (): Base model class
        PasswordMixin (): Password mixin class
    """

    __tablename__ = "doctors"
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                            nullable=False)
    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), index=True, unique=True, nullable=False
    )
    certificates: so.Mapped[str] = so.mapped_column(sa.String(256))
    phone: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(10), index=True, unique=True
    )
    department_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("departments.id"), index=True,
        nullable=False
    )
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256),
                                                     nullable=False)
    department: so.Mapped["Department"] = so.relationship(
        "Department", back_populates="doctors"
    )
    appointments: so.Mapped[List["Appointment"]] = so.relationship(
        "Appointment", back_populates="doctor"
    )
    timeslots: so.Mapped[List["TimeSlot"]] = so.relationship(
        "TimeSlot", back_populates="doctor"
    )
