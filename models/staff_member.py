from typing import Optional
from utils import PasswordMixin, SearchableMixin
import sqlalchemy.orm as so
import sqlalchemy as sa
import models as m
from .base_model import BaseModel, gen_datetime
from flask_login import UserMixin

class StaffMember(BaseModel, PasswordMixin, SearchableMixin, UserMixin):
    __abstract__ = True
    __searchable__ = ["name", "phone", "email"]

    def __init__(self, password: str, **kwargs):
        """
        Constructor for the Doctor class
        Args:
            passwd (str): Password for the doctor
            **kwargs: Arbitrary keyword arguments
        """
        PasswordMixin.__init__(self, password)
        super().__init__(**kwargs)


    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), index=True, unique=True, nullable=False
    )

    name: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True, nullable=False
    )

    password_hash: so.Mapped[str] = so.mapped_column(
        sa.String(256), nullable=False
    )

    is_active: so.Mapped[sa.Boolean] = so.mapped_column(
        sa.Boolean, default=True
    )

    phone: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(10), index=True, unique=True
    )

    last_seen: so.Mapped[Optional[sa.DateTime]] = so.mapped_column(
        sa.DateTime(timezone=True), default=gen_datetime
    )
