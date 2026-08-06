from cryptography.fernet import Fernet


def generate_key() -> bytes:
    """
    Generate and return a new Fernet encryption key.
    """
    return Fernet.generate_key()


def encrypt_file(
    input_file: str,
    output_file: str,
    key: bytes,
) -> None:
    """
    Encrypt a file using a Fernet key.

    Args:
        input_file: Path to the original file.
        output_file: Path where the encrypted file will be saved.
        key: Fernet encryption key.
    """

    fernet = Fernet(key)

    with open(input_file, "rb") as file:
        file_data = file.read()

    encrypted_data = fernet.encrypt(file_data)

    with open(output_file, "wb") as file:
        file.write(encrypted_data)


def decrypt_file(
    input_file: str,
    output_file: str,
    key: bytes,
) -> None:
    """
    Decrypt a Fernet encrypted file.

    Args:
        input_file: Path to the encrypted file.
        output_file: Path where the decrypted file will be saved.
        key: Fernet encryption key.
    """

    fernet = Fernet(key)

    with open(input_file, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    with open(output_file, "wb") as file:
        file.write(decrypted_data)