import models as m
from .base_model import BaseModel
import sqlalchemy as sa
import sqlalchemy.orm as so
from enum import Enum


class TimeSlotStatus(str, Enum):
    AVAILABLE = "available"
    BOOKED = "booked"


class TimeSlot(BaseModel):
    __tablename__ = "timeslots"
    __table_args__ = (
        sa.UniqueConstraint(
            "doctor_id", "date", "start_time", name="doctor_date_startTime_uc"
        ),
        sa.CheckConstraint("end_time > start_time", name="check_time_validity")
    )
    doctor_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("doctors.id"), index=True
    )
    date: so.Mapped[sa.Date] = so.mapped_column(sa.Date, index=True,
                                                nullable=False)
    start_time: so.Mapped[sa.Time] = so.mapped_column(
        sa.Time, index=True, nullable=False
    )
    end_time: so.Mapped[sa.Time] = so.mapped_column(sa.Time, index=True,
                                                    nullable=False)
    doctor: so.Mapped["m.Doctor"] = so.relationship("Doctor",
                                                    back_populates="timeslots")
    status: so.Mapped[TimeSlotStatus] = so.mapped_column(
        sa.Enum(TimeSlotStatus),
        index=True,
        nullable=False,
        default=TimeSlotStatus.AVAILABLE,
    )
