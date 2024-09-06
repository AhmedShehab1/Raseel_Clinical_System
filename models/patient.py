from enum import Enum
from time import time
from typing import List, Optional
import models as m
from .base_model import BaseModel, gen_datetime
import sqlalchemy as sa
import sqlalchemy.orm as so
from utils import PasswordMixin
from flask_login import UserMixin
import jwt
from web_flask import db
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date
from flask import current_app
from utils.search_util import SearchableMixin

class GenderType(str, Enum):
    Male = "male"
    Female = "female"


class Patient(BaseModel, PasswordMixin, UserMixin, SearchableMixin):
    """
    Patient model class
    Args:
        BaseModel (): Base model class
    """
    __searchable__ = ['name', 'email', 'contact_number', 'national_id']

    def __init__(self, password: str, **kwargs):
        """
        Constructor for the Patient class
        Args:
            password (str): Password for the patient
            **kwargs: Arbitrary keyword arguments
        """
        PasswordMixin.__init__(self, password)
        super().__init__(**kwargs)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config["SECRET_KEY"],
                            algorithms=["HS256"])[
                "reset_password"
            ]
            return db.session.get(Patient, id)
        except Exception:
            return None

    __tablename__ = "patients"
    name: so.Mapped[str] = so.mapped_column(sa.String(64),
                                            index=True,
                                            nullable=False)

    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), index=True, unique=True, nullable=False
    )

    contact_number: so.Mapped[str] = so.mapped_column(
        sa.String(10), index=True, unique=True, nullable=False
    )

    birth_date: so.Mapped[sa.Date] = so.mapped_column(sa.Date)

    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256),
                                                     nullable=False)

    address: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    national_id: so.Mapped[str] = so.mapped_column(sa.String(10), unique=True, nullable=False)

    gender: so.Mapped[GenderType] = so.mapped_column(sa.Enum(GenderType), nullable=False)

    medical_history: so.Mapped[Optional[str]] = so.mapped_column(sa.String(400))

    current_medications: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    department_id: so.Mapped[Optional[str]] = so.mapped_column(
        sa.ForeignKey("departments.id")
    )

    department: so.Mapped["m.Department"] = so.relationship(
        "Department", back_populates="patients"
    )

    appointments: so.Mapped[List["m.Appointment"]] = so.relationship(
        "Appointment", back_populates="patient"
    )

    last_seen: so.Mapped[Optional[sa.DateTime]] = so.mapped_column(
        sa.DateTime, default=gen_datetime
    )


    vitals: so.Mapped[List["m.Vital"]] = so.relationship("Vital", back_populates="patient")

    diagnoses: so.Mapped[List["m.Diagnose"]] = so.relationship("Diagnose", back_populates="patient")

    prescriptions: so.Mapped[List["m.Prescription"]] = so.relationship("Prescription", back_populates="patient")

    allergies: so.Mapped[List["m.Allergy"]] = so.relationship("Allergy", back_populates="patient")

    @hybrid_property
    def age(self):
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )


class Vital(BaseModel):
    """
    Vital model class
    Args:
        BaseModel (): Base model class
    """


    __tablename__ = "vitals"
    patient_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("patients.id"), index=True, nullable=False
    )
    patient: so.Mapped["m.Patient"] = so.relationship("Patient", back_populates="vitals")
    height: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    weight: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    temperature: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    blood_pressure: so.Mapped[str] = so.mapped_column(sa.String(10), nullable=False)
    pulse: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)


    @property
    def vitals_list(self):
        return [
            ("Height", self.height),
            ("Weight", self.weight),
            ("Temperature", self.temperature),
            ("Blood Pressure", self.blood_pressure),
            ("Pulse", self.pulse),
        ]

    @hybrid_property
    def bmi(self):
        return self.weight / (self.height ** 2)

    @hybrid_property
    def status(self):
        if self.temperature > 100 or self.blood_pressure > 140 or self.blood_pressure < 90 or self.pulse > 100 or self.pulse < 60 or self.bmi > 25:
            return "Critical"
        return "Normal"

    @hybrid_property
    def status_color(self):
        if self.status == "Critical":
            return "danger"
        return "success"

    @hybrid_property
    def status_icon(self):
        if self.status == "Critical":
            return "fa-exclamation-triangle"
        return "fa-check-circle"

    @hybrid_property
    def status_text(self):
        if self.status == "Critical":
            return "Critical"
        return "Normal"

class Diagnose(BaseModel):
    """
    Diagnose model class
    Args:
        BaseModel (): Base model class
    """
    __tablename__ = "diagnoses"
    __table_args__ = (sa.UniqueConstraint("patient_id", "diagnose_name", name="uq_patient_diagnose"),)

    patient_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("patients.id"), index=True, nullable=False
    )
    patient: so.Mapped["m.Patient"] = so.relationship("Patient", back_populates="diagnoses")
    name: so.Mapped[Optional[str]] = so.mapped_column("diagnose_name", sa.String(256))


class Prescription(BaseModel):
    """
    Prescription model class
    Args:
        BaseModel (): Base model class
    """

    __tablename__ = "prescriptions"
    patient_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("patients.id"), index=True, nullable=False
    )
    patient: so.Mapped["m.Patient"] = so.relationship("Patient", back_populates="prescriptions")
    medication: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=True)
    dosage: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=True)


class Allergy(BaseModel):
    """
    Allergy model class
    Args:
        BaseModel (): Base model class
    """
    __tablename__ = "allergies"
    __table_args__ = (sa.UniqueConstraint("patient_id", "allergen", name="uq_patient_allergy"),)
    patient_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("patients.id"), index=True, nullable=False
    )
    patient: so.Mapped["m.Patient"] = so.relationship("Patient", back_populates="allergies")
    allergen: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    reaction: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)

