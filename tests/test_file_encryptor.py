import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.file_encryptor import generate_key


def test_generate_key():
    key = generate_key()

    assert isinstance(key, bytes)
    assert len(key) == 44