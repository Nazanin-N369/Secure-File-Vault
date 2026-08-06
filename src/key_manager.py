def save_key(key: bytes, file_path: str) -> None:
    """
    Save encryption key to a file.
    """
    with open(file_path, "wb") as file:
        file.write(key)


def load_key(file_path: str) -> bytes:
    """
    Load encryption key from a file.
    """
    with open(file_path, "rb") as file:
        return file.read()