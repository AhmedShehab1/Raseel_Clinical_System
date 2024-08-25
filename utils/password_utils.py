from werkzeug.security import generate_password_hash, check_password_hash


class PasswordMixin:
    """
    Password mixin class
    """
    password_hash = None

    def __init__(self, passwd: str):
        """
        initializes the password hash
        Args:
            passwd (str): password to be hashed
        """
        self.set_password(passwd)

    def set_password(self, passwd: str):
        """
        sets the password hash for the patient
        Args:
            passwd (str): password to be hashed
        """
        self.password_hash = generate_password_hash(passwd)

    def check_password(self, passwd: str) -> bool:
        """
        checks if the password is correct
        Args:
            passwd (str): password to be verified

        Returns:
            bool: True if password is correct, False otherwise
        """
        return check_password_hash(self.password_hash, passwd)
