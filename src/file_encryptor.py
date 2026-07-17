from cryptography.fernet import Fernet


def generate_key() -> bytes:
    """
    Generate a new Fernet encryption key.
    """
    return Fernet.generate_key()


def encrypt_file(
    input_file: str,
    output_file: str,
    key: bytes,
) -> None:
    """
    Encrypt a file using Fernet.
    """

    fernet = Fernet(key)

    with open(input_file, "rb") as file:
        data = file.read()

    encrypted_data = fernet.encrypt(data)

    with open(output_file, "wb") as file:
        file.write(encrypted_data)