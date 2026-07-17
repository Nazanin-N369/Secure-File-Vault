
from src.file_hasher import calculate_file_hash


def verify_file_integrity(file_path: str, expected_hash: str) -> bool:
    """
    Verify that a file matches the expected SHA-256 hash.
    """
    current_hash = calculate_file_hash(file_path)

    return current_hash == expected_hash