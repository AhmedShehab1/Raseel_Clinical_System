from typing import List
import models as m
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin


class Doctor(m.StaffMember):
    """
    Doctor model class
    Args:
        BaseModel (): Base model class
        PasswordMixin (): Password mixin class
    """

    __tablename__ = "doctors"

    certificates: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False)

    department_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("departments.id"), index=True, nullable=False
    )

    department: so.Mapped["m.Department"] = so.relationship(
        "Department", back_populates="doctors"
    )
    appointments: so.Mapped[List["m.Appointment"]] = so.relationship(
        "Appointment", back_populates="doctor"
    )

    working_hours: so.Mapped[List["m.WorkingHours"]] = so.relationship(
        "WorkingHours", back_populates="doctor"
    )
