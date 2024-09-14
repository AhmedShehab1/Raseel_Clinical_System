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
