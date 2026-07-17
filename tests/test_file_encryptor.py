import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.file_encryptor import generate_key


def test_generate_key():
    key = generate_key()

    assert isinstance(key, bytes)
    assert len(key) == 44
    
    

import tempfile

from src.file_encryptor import (
    generate_key,
    encrypt_file,
)


def test_encrypt_file():

    with tempfile.NamedTemporaryFile(
        mode="wb",
        delete=False,
    ) as file:

        file.write(b"Hello World")

        input_path = file.name

    output_path = input_path + ".enc"

    key = generate_key()

    encrypt_file(
        input_path,
        output_path,
        key,
    )

    assert Path(output_path).exists()