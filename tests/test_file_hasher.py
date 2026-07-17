from src.file_hasher import calculate_file_hash
import tempfile


def test_file_hash():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as file:
        file.write("Hello World")
        path = file.name

    hash_value = calculate_file_hash(path)

    assert len(hash_value) == 64