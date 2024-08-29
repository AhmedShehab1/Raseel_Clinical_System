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
        except Exception:
            return
        return db.session.get(Patient, id)

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

    @hybrid_property
    def age(self):
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )
