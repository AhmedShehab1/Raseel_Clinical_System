from typing import List, Optional
import models as m
from .base_model import BaseModel, gen_datetime
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

    def __init__(self, passwd: str, **kwargs):
        """
        Constructor for the Doctor class
        Args:
            passwd (str): Password for the doctor
            **kwargs: Arbitrary keyword arguments
        """
        PasswordMixin.__init__(self, passwd)
        super().__init__(**kwargs)

    __tablename__ = "doctors"
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                            nullable=False)
    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), index=True, unique=True, nullable=False
    )
    certificates: so.Mapped[str] = so.mapped_column(sa.String(256),
                                                    nullable=False)

    phone: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(10), index=True, unique=True
    )

    department_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("departments.id"), index=True,
        nullable=False
    )

    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256),
                                                     nullable=False)

    department: so.Mapped["m.Department"] = so.relationship(
        "Department", back_populates="doctors"
    )
    appointments: so.Mapped[List["m.Appointment"]] = so.relationship(
        "Appointment", back_populates="doctor"
    )
    timeslots: so.Mapped[List["m.TimeSlot"]] = so.relationship(
        "TimeSlot", back_populates="doctor"
    )
    last_seen: so.Mapped[Optional[sa.DateTime]] = so.mapped_column(
        sa.DateTime, default=gen_datetime
    )
