import sys
from pathlib import Path
import tempfile

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.file_encryptor import generate_key
from src.key_manager import save_key, load_key


def test_save_and_load_key():

    key = generate_key()

    with tempfile.NamedTemporaryFile(delete=False) as file:
        key_path = file.name

    save_key(key, key_path)

    loaded_key = load_key(key_path)

    assert loaded_key == key