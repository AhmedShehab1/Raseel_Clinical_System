from enum import Enum
from .base_model import BaseModel
import sqlalchemy as sa
import sqlalchemy.orm as so


class DayOfWeek(str, Enum):
    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"


class WorkingHours(BaseModel):
    __tablename__ = "working_hours"
    __table_args__ = (
        sa.PrimaryKeyConstraint("doctor_id", "day"),
        sa.CheckConstraint("end_time > start_time", name="check_time_validity"),
    )
    id = None

    doctor_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey("doctors.id"), index=True, nullable=False
    )

    doctor: so.Mapped["m.Doctor"] = so.relationship(
        "Doctor", back_populates="working_hours"
    )

    start_time: so.Mapped[sa.Time] = so.mapped_column(
        sa.Time, index=True, nullable=False
    )

    end_time: so.Mapped[sa.Time] = so.mapped_column(sa.Time, index=True, nullable=False)

    day: so.Mapped[DayOfWeek] = so.mapped_column(
        sa.Enum(DayOfWeek), index=True, nullable=False
    )
