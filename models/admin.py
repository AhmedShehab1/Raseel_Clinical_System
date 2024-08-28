import models as m


class Admin(m.StaffMember):
    """
    Admin model class
    Args:
        BaseModel (): Base model class
    """

    __tablename__ = "admins"
