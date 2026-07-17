from cryptography.fernet import Fernet


def generate_key() -> bytes:
    """
    Generate a new Fernet encryption key.
    """
    return Fernet.generate_key()