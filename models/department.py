from typing import List
from models.base_model import BaseModel
from models.doctor import Doctor
from models.patient import Patient
import sqlalchemy as sa
import sqlalchemy.orm as so


class Department(BaseModel):
    __tablename__ = "departments"
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                            nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.String(256))
    doctors: so.Mapped[List["Doctor"]] = so.relationship(
        "Doctor", back_populates="department",
        cascade="all, delete, delete-orphan"
    )
    patients: so.Mapped[List["Patient"]] = so.relationship(
        "Patient", back_populates="department",
        cascade="all, delete-orphan"
    )
