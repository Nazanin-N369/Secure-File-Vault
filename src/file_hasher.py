import hashlib


CHUNK_SIZE = 8192


def calculate_file_hash(file_path: str) -> str:
    """
    Calculate SHA-256 hash of a file.
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(CHUNK_SIZE):
            sha256.update(chunk)

    return sha256.hexdigest()