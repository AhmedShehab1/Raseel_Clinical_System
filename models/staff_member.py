from typing import Optional
from utils import PasswordMixin
from sqlalchemy.ext.declarative import declared_attr
import sqlalchemy.orm as so
import sqlalchemy as sa
import models as m
from .base_model import BaseModel, gen_datetime


class StaffMember(BaseModel, PasswordMixin):
    __abstract__ = True

    def __init__(self, password: str, **kwargs):
        """
        Constructor for the Doctor class
        Args:
            passwd (str): Password for the doctor
            **kwargs: Arbitrary keyword arguments
        """
        PasswordMixin.__init__(self, password)
        super().__init__(**kwargs)

    @declared_attr
    def name(cls) -> so.Mapped[str]:
        return so.mapped_column(sa.String(64), index=True, nullable=False)

    @declared_attr
    def password_hash(cls) -> so.Mapped[str]:
        return so.mapped_column(sa.String(256), nullable=False)

    @declared_attr
    def is_active(cls) -> so.Mapped[sa.Boolean]:
        return so.mapped_column(sa.Boolean, default=True)

    @declared_attr
    def phone(cls) -> so.Mapped[Optional[str]]:
        return so.mapped_column(sa.String(10), index=True, unique=True)

    @declared_attr
    def last_seen(cls) -> so.Mapped[Optional[sa.DateTime]]:
        return so.mapped_column(sa.DateTime, default=gen_datetime)
