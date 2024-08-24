from typing import List
import models as m
from .base_model import BaseModel
import sqlalchemy as sa
import sqlalchemy.orm as so


class Department(BaseModel):
    __tablename__ = "departments"
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                            nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.String(256))
    doctors: so.Mapped[List["m.Doctor"]] = so.relationship(
        "Doctor", back_populates="department"
    )
    patients: so.Mapped[List["m.Patient"]] = so.relationship(
        "Patient", back_populates="department"
    )
