from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from web_flask import db
import uuid
from datetime import datetime, timezone

time = "%Y-%m-%dT%H:%M:%S.%f"

def gen_datetime():
    """
    Generate the current datetime in UTC timezone
    Returns:
        datetime: current datetime in UTC timezone
    """
    return datetime.now(timezone.utc)


class BaseModel(db.Model):
    """
    Base model class
    Args:
        db (): Database object
    """

    __abstract__ = True
    id: so.Mapped[str] = so.mapped_column(
        sa.String(128), primary_key=True, default=lambda: str(uuid.uuid4()),
        index=True
    )
    created_at: so.Mapped[sa.DateTime] = so.mapped_column(
        sa.DateTime, default=gen_datetime
    )
    updated_at: so.Mapped[sa.DateTime] = so.mapped_column(
        sa.DateTime, default=gen_datetime, onupdate=gen_datetime
    )
    deleted_at: so.Mapped[Optional[sa.DateTime]] = so.mapped_column(
        sa.DateTime, nullable=True
    )

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(
            self.__class__.__name__, self.id, self.__dict__
        )

    def to_dict(self):
        new_dict = self.__dict__.copy()
        if 'created_at' in new_dict:
            new_dict['created_at'] = new_dict['created_at'].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)

        new_dict["__class__"] = self.__class__.__name__

        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        for key, value in new_dict.items():
            if isinstance(value, BaseModel):
                new_dict[key] = value.to_dict()
            elif isinstance(value, list) and all(isinstance(i, BaseModel) for i in value):
                new_dict[key] = [i.to_dict() for i in value]
            elif isinstance(value, dict) and all(isinstance(i, BaseModel) for i in value.values()):
                new_dict[key] = {k: v.to_dict() for k, v in value.items()}

        return new_dict
