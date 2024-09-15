from enum import Enum
from time import time
from typing import List, Optional
import models as m
from .base_model import BaseModel, gen_datetime
import sqlalchemy as sa
import sqlalchemy.orm as so
from utils import PasswordMixin, SearchableMixin
from flask_login import UserMixin
import jwt
from web_flask import db
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date, datetime
from flask import current_app
from datetime import timezone



class GenderType(str, Enum):
    Male = "male"
    Female = "female"


class Patient(BaseModel, PasswordMixin, SearchableMixin, UserMixin):
    """
    Patient model class
    Args:
        BaseModel (): Base model class
    """
    __abstract__ = False
    __tablename__ = "patients"
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
        sa.DateTime(timezone=True), default=gen_datetime
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
    measured_at: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime(timezone=True), default=datetime.now(timezone.utc))


    @property
    def vitals_list(self):
        return [
            ("Height", self.height, "Normal", "success", "fa-check-circle"),
            ("Weight", self.weight, "Normal", "success", "fa-check-circle"),
            ("Temperature", self.temperature, self.status_temp, self.status_color_temp, self.status_icon_temp),
            ("Blood Pressure", self.blood_pressure, self.status_blood_pressure, self.status_color_blood_pressure, self.status_icon_blood_pressure),
            ("Pulse", self.pulse, self.status_pulse, self.status_color_pulse, self.status_icon_pulse),
            ("BMI", self.bmi, self.status_bmi, self.status_color_bmi, self.status_icon_bmi),
        ]

    @hybrid_property
    def bmi(self):
        height_in_meters = self.height / 100
        return round(self.weight / (height_in_meters ** 2), 2)

    @hybrid_property
    def status_temp(self):
        if self.temperature > 100:
            return "Critical"
        return "Normal"

    @hybrid_property
    def status_color_temp(self):
        return "danger" if self.status_temp == "Critical" else "success"

    @hybrid_property
    def status_icon_temp(self):
        return "fa-exclamation-triangle" if self.status_temp == "Critical" else "fa-check-circle"

    @hybrid_property
    def status_pulse(self):
        if self.pulse > 100 or self.pulse < 60:
            return "Critical"
        return "Normal"

    @hybrid_property
    def status_icon_pulse(self):
        return "fa-exclamation-triangle" if self.status_pulse == "Critical" else "fa-check-circle"

    @hybrid_property
    def status_color_pulse(self):
        return "danger" if self.status_pulse == "Critical" else "success"


    @hybrid_property
    def status_bmi(self):
        if self.bmi > 25:
            return "Critical"
        return "Normal"

    @hybrid_property
    def status_color_bmi(self):
        return "danger" if self.status_bmi == "Critical" else "success"

    @hybrid_property
    def status_icon_bmi(self):
        return "fa-exclamation-triangle" if self.status_bmi == "Critical" else "fa-check-circle"

    @hybrid_property
    def systolic_bp(self):
        return int(self.blood_pressure.split('/')[0])

    @hybrid_property
    def diastolic_bp(self):
        return int(self.blood_pressure.split('/')[1])

    @hybrid_property
    def status_blood_pressure(self):
        if self.systolic_bp in range(90, 141) and self.diastolic_bp in range(60, 91):
            return "Normal"
        return "Critical"

    @hybrid_property
    def status_color_blood_pressure(self):
        return "danger" if self.status_blood_pressure == "Critical" else "success"

    @hybrid_property
    def status_icon_blood_pressure(self):
        return "fa-exclamation-triangle" if self.status_blood_pressure == "Critical" else "fa-check-circle"


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
