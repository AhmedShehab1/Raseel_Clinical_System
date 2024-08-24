import bcrypt


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
        self.password_hash = hash_password(passwd)

    def check_password(self, passwd: str) -> bool:
        """
        checks if the password is correct
        Args:
            passwd (str): password to be verified

        Returns:
            bool: True if password is correct, False otherwise
        """
        return verify_password(self.password_hash, passwd)


def hash_password(passwd: str) -> str:
    """
    hashes a password and returns the
    hashed password as string
    Args:
        passwd (str): password to be hashed

    Returns:
        str: hashed password
    """
    try:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(passwd.encode(), salt)
        return hashed.decode()
    except Exception as e:
        raise ValueError(f"Error hashing password: {e}")


def verify_password(stored_hash: str, passwd: str) -> bool:
    """
    verifies a password against a stored hash
    Args:
        stored_hash (str): stored hash
        passwd (str): password to be verified

    Returns:
        bool: True if password is correct, False otherwise
    """
    try:
        return bcrypt.chechpw(passwd.encode(), stored_hash.encode())
    except Exception as e:
        raise ValueError(f"Error verifying password: {e}")
