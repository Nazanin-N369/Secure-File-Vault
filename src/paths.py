
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_DIR = PROJECT_ROOT / "input"
VAULT_DIR = PROJECT_ROOT / "vault-result"


def ensure_vault_exists() -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    VAULT_DIR.mkdir(parents=True, exist_ok=True)


def ensure_directories_exist() -> None:
    ensure_vault_exists()


def create_case_folder(file_name: str) -> Path:
    ensure_vault_exists()

    stem = Path(file_name).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    case_folder = VAULT_DIR / f"{stem}_{timestamp}"
    case_folder.mkdir(parents=True, exist_ok=True)

    return case_folder


def find_latest_case_folder(file_name: str) -> Path | None:
    ensure_vault_exists()

    stem = Path(file_name).stem

    matching_folders = sorted(
        (
            path
            for path in VAULT_DIR.glob(f"{stem}_*")
            if path.is_dir()
        ),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    return matching_folders[0] if matching_folders else None