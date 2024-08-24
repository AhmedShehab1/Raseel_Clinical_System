from typing import List
import models as m
from .base_model import BaseModel
import sqlalchemy as sa
import sqlalchemy.orm as so
from utils import PasswordMixin
from flask_login import UserMixin


class Patient(BaseModel, PasswordMixin, UserMixin):
    """
    Patient model class
    Args:
        BaseModel (): Base model class
    """
    def __init__(self, password: str, **kwargs):
        """
        Constructor for the Patient class
        Args:
            passwd (str): Password for the patient
            **kwargs: Arbitrary keyword arguments
        """
        PasswordMixin.__init__(self, password)
        super().__init__(**kwargs)

    __tablename__ = "patients"
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                            nullable=False)
    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), index=True, unique=True, nullable=False
    )
    contact_number: so.Mapped[str] = so.mapped_column(
        sa.String(10), index=True, unique=True, nullable=False
    )
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256),
                                                     nullable=False)
    address: so.Mapped[str] = so.mapped_column(sa.String(256),
                                               nullable=True)
    medical_history: so.Mapped[str] = so.mapped_column(sa.String(400),
                                                       nullable=True)
    current_medications: so.Mapped[str] = so.mapped_column(sa.String(256),
                                                           nullable=True)
    department_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("departments.id"), nullable=True
    )
    department: so.Mapped["m.Department"] = so.relationship(
        "Department", back_populates="patients"
    )
    appointments: so.Mapped[List["m.Appointment"]] = so.relationship(
        "Appointment", back_populates="patient"
    )
