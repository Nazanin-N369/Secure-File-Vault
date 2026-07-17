import sys
from pathlib import Path
import tempfile

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.file_hasher import calculate_file_hash
from src.integrity_checker import verify_file_integrity


def test_verify_file_integrity():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as file:
        file.write("Hello World")
        path = file.name

    expected_hash = calculate_file_hash(path)

    assert verify_file_integrity(path, expected_hash)