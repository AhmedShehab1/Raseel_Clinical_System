import models as m


class Receptionist(m.StaffMember):
    """
    Receptionist model class
    Args:
        BaseModel (): Base model class
        PasswordMixin (): Password mixin class
    """

    __tablename__ = "receptionists"
