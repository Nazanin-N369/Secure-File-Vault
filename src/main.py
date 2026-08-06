from src.cli import run
from src.paths import ensure_vault_exists



ensure_vault_exists()


if __name__ == "__main__":
    try:
        run()

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        print("Goodbye!")