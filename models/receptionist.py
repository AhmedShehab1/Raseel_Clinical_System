from typing import List
import models as m
import sqlalchemy as sa
import sqlalchemy.orm as so


class Receptionist(m.StaffMember):
    """
    Receptionist model class
    Args:
        BaseModel (): Base model class
        PasswordMixin (): Password mixin class
    """

    __tablename__ = "receptionists"

    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), index=True, unique=True, nullable=False
    )

    appointments: so.Mapped[List["m.Appointment"]] = so.relationship(
        "Appointment", back_populates="doctor"
    )

    timeslots: so.Mapped[List["m.TimeSlot"]] = so.relationship(
        "TimeSlot", back_populates="doctor"
    )

    working_hours: so.Mapped[List["m.WorkingHours"]] = so.relationship(
        "WorkingHours", back_populates="doctor"
    )
