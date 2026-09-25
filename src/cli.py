from pathlib import Path
import os
import sys
import time

from src.key_manager import load_key, save_key

from src.file_encryptor import generate_key, encrypt_file, decrypt_file

from src.file_hasher import calculate_file_hash

from src.integrity_checker import verify_file_integrity

from src.paths import (
    INPUT_DIR,
    create_case_folder,
    find_latest_case_folder,
    ensure_directories_exist,
)


# ============================================================
# TERMINAL THEME
# ============================================================

RESET = "\033[0m"

BOLD = "\033[1m"
DIM = "\033[2m"

BLACK = "\033[30m"
WHITE = "\033[97m"
GRAY = "\033[90m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"

# Main cyber palette
PRIMARY = CYAN
ACCENT = MAGENTA
SUCCESS = GREEN
WARNING = YELLOW
ERROR = RED
INFO = BLUE


# ============================================================
# WINDOWS ANSI SUPPORT
# ============================================================

def enable_windows_ansi():
    """
    Enable ANSI escape sequences in Windows terminals.

    This only affects terminal rendering and does not change
    application functionality.
    """
    if os.name != "nt":
        return

    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32

        stdout_handle = kernel32.GetStdHandle(-11)

        mode = ctypes.c_uint32()

        if kernel32.GetConsoleMode(
            stdout_handle,
            ctypes.byref(mode),
        ):
            kernel32.SetConsoleMode(
                stdout_handle,
                mode.value | 0x0004,
            )

    except Exception:
        pass


enable_windows_ansi()


# Disable colors when output is redirected or ANSI is unavailable.
USE_COLOR = sys.stdout.isatty()

if not USE_COLOR:
    RESET = ""
    BOLD = ""
    DIM = ""

    BLACK = ""
    WHITE = ""
    GRAY = ""

    RED = ""
    GREEN = ""
    YELLOW = ""
    BLUE = ""
    MAGENTA = ""
    CYAN = ""

    PRIMARY = ""
    ACCENT = ""
    SUCCESS = ""
    WARNING = ""
    ERROR = ""
    INFO = ""


# ============================================================
# DISPLAY HELPERS
# ============================================================

def clear_screen():
    """
    Clear the terminal screen.

    Presentation only.
    """
    if not sys.stdout.isatty():
        return

    os.system("cls" if os.name == "nt" else "clear")


def type_text(text: str, delay: float = 0.008):
    """
    Small terminal typing effect.

    Used only for visual presentation.
    """
    if not USE_COLOR or not sys.stdout.isatty():
        print(text)
        return

    for character in text:
        print(character, end="", flush=True)
        time.sleep(delay)

    print()


def status(message: str, symbol: str = "•"):
    print(
        f"{DIM}{GRAY}[{RESET}"
        f"{PRIMARY}{symbol}{RESET}"
        f"{DIM}{GRAY}]{RESET} "
        f"{WHITE}{message}{RESET}"
    )


def success(message: str):
    print(
        f"{SUCCESS}{BOLD}[+]{RESET} "
        f"{WHITE}{message}{RESET}"
    )


def error(message: str):
    print(
        f"{ERROR}{BOLD}[-]{RESET} "
        f"{WHITE}{message}{RESET}"
    )


def warning(message: str):
    print(
        f"{WARNING}{BOLD}[!]{RESET} "
        f"{WHITE}{message}{RESET}"
    )


def info(message: str):
    print(
        f"{INFO}{BOLD}[*]{RESET} "
        f"{WHITE}{message}{RESET}"
    )


def animated_status(message: str):
    """
    Very short visual status animation.

    It does not perform or modify any application operation.
    """
    if not USE_COLOR or not sys.stdout.isatty():
        info(message)
        return

    print(
        f"{PRIMARY}{BOLD}[*]{RESET} "
        f"{WHITE}{message}",
        end="",
        flush=True,
    )

    for _ in range(3):
        time.sleep(0.12)
        print(".", end="", flush=True)

    print(f" {SUCCESS}OK{RESET}")


def section_title(title: str):
    print()
    print(
        f"{PRIMARY}{BOLD}"
        f"─── {RESET}"
        f"{WHITE}{BOLD}{title}{RESET}"
        f" {PRIMARY}{BOLD}────────────────────────────{RESET}"
    )


def wait_for_enter():
    input(
        f"\n{DIM}{GRAY}"
        f"Press Enter to continue..."
        f"{RESET}"
    )


# ============================================================
# BANNER
# ============================================================

def show_banner():
    print(
        f"{PRIMARY}{BOLD}"
"        ╭──────────────────────────╮\n"
"        │      SECURE FILE VAULT   │\n"
"        │                          │\n"
"        │        ┌────────┐        │\n"
"        │        │  ████  │        │\n"
"        │        │  ████  │        │\n"
"        │        └───┬────┘        │\n"
"        │            │             │\n"
"        │       FILE PROTECTED     │\n"
"        ╰──────────────────────────╯"
f"{RESET}"
    )

    print()
    print(
        f"        {WHITE}{BOLD} BY NAZANIN NAROUEI {RESET}"
    )
    print()
    print(
        f"        {DIM}{PRIMARY}"
        f"CYBERSECURITY FILE PROTECTION SYSTEM"
        f"{RESET}"
    )

    print(
        f"        {DIM}{GRAY}"
        f"────────────────────────────────"
        f"{RESET}"
    )

    print()


# ============================================================
# MENU
# ============================================================

def show_menu():
    print(
        f"{PRIMARY}{BOLD}"
        "  ┌────────────────────────────────────────────┐"
        f"{RESET}"
    )

    print(
        f"  {PRIMARY}{BOLD}│{RESET} "
        f"{WHITE}{BOLD}VAULT OPERATIONS{RESET}"
        f"                         "
        f"{PRIMARY}{BOLD}│{RESET}"
    )

    print(
        f"  {PRIMARY}{BOLD}├────────────────────────────────────────────┤"
        f"{RESET}"
    )

    print(
        f"  {PRIMARY}{BOLD}│{RESET} "
        f"{GREEN}{BOLD}[1]{RESET} "
        f"{WHITE}Encrypt File{RESET}"
        f"                           "
        f"{PRIMARY}{BOLD}│{RESET}"
    )

    print(
        f"  {PRIMARY}{BOLD}│{RESET} "
        f"{CYAN}{BOLD}[2]{RESET} "
        f"{WHITE}Decrypt File{RESET}"
        f"                           "
        f"{PRIMARY}{BOLD}│{RESET}"
    )

    print(
        f"  {PRIMARY}{BOLD}│{RESET} "
        f"{BLUE}{BOLD}[3]{RESET} "
        f"{WHITE}Calculate File Hash{RESET}"
        f"                   "
        f"{PRIMARY}{BOLD}│{RESET}"
    )

    print(
        f"  {PRIMARY}{BOLD}│{RESET} "
        f"{MAGENTA}{BOLD}[4]{RESET} "
        f"{WHITE}Verify File Integrity{RESET}"
        f"                 "
        f"{PRIMARY}{BOLD}│{RESET}"
    )

    print(
        f"  {PRIMARY}{BOLD}│{RESET} "
        f"{RED}{BOLD}[0]{RESET} "
        f"{WHITE}Exit{RESET}"
        f"                                    "
        f"{PRIMARY}{BOLD}│{RESET}"
    )

    print(
        f"{PRIMARY}{BOLD}"
        "  └────────────────────────────────────────────┘"
        f"{RESET}"
    )


def get_menu_choice():
    return input(
        f"\n{PRIMARY}{BOLD}"
        "  VAULT"
        f"{RESET}"
        f"{GRAY} > {RESET}"
    ).strip()


# ============================================================
# INPUT FILE
# ============================================================

def get_input_file() -> Path | None:
    ensure_directories_exist()

    section_title("INPUT FILE")

    print(
        f"{GRAY}Enter the name of the file in the input folder."
        f"{RESET}"
    )

    print(
        f"{GRAY}Example:{RESET} "
        f"{WHITE}secret.txt{RESET}"
    )

    file_name = input(
        f"\n{PRIMARY}{BOLD}"
        "File name"
        f"{RESET}"
        f"{GRAY} > {RESET}"
    ).strip()

    if not file_name:
        error("File name cannot be empty.")
        return None

    if Path(file_name).name != file_name:
        error("Please enter a file name only, not a path.")
        return None

    input_file = INPUT_DIR / file_name

    if not input_file.is_file():
        error(
            f"File not found in input folder: "
            f"{WHITE}{file_name}{RESET}"
        )
        return None

    success(
        f"Input file detected: "
        f"{CYAN}{file_name}{RESET}"
    )

    return input_file


# ============================================================
# ENCRYPT
# ============================================================

def encrypt_file_flow():
    clear_screen()
    show_banner()

    section_title("ENCRYPT FILE")

    input_file = get_input_file()

    if input_file is None:
        wait_for_enter()
        return

    animated_status("Generating encryption key")

    key = generate_key()

    case_folder = create_case_folder(input_file.name)

    encrypted_path = case_folder / f"{input_file.name}.enc"
    key_path = case_folder / f"{input_file.stem}.key"
    hash_path = case_folder / f"{input_file.stem}.sha256"

    animated_status("Encrypting file")

    encrypt_file(
        str(input_file),
        str(encrypted_path),
        key,
    )

    animated_status("Saving encryption key")

    save_key(
        key,
        str(key_path),
    )

    animated_status("Calculating SHA-256 hash")

    file_hash = calculate_file_hash(str(input_file))

    with open(hash_path, "w", encoding="utf-8") as file:
        file.write(file_hash)

    print()

    success("File encrypted successfully.")

    print()
    print(
        f"{PRIMARY}{BOLD}"
        "  VAULT OUTPUT"
        f"{RESET}"
    )

    print(
        f"  {GRAY}Result folder{RESET}"
        f"   : {WHITE}{case_folder.name}{RESET}"
    )

    print(
        f"  {GRAY}Encrypted file{RESET}"
        f"  : {WHITE}{encrypted_path.name}{RESET}"
    )

    print(
        f"  {GRAY}Encryption key{RESET}"
        f"  : {WHITE}{key_path.name}{RESET}"
    )

    print(
        f"  {GRAY}SHA-256 hash{RESET}"
        f"    : {WHITE}{hash_path.name}{RESET}"
    )

    wait_for_enter()


# ============================================================
# DECRYPT
# ============================================================

def decrypt_file_flow():
    clear_screen()
    show_banner()

    section_title("DECRYPT FILE")

    input_file = get_input_file()

    if input_file is None:
        wait_for_enter()
        return

    case_folder = find_latest_case_folder(input_file.name)

    if case_folder is None:
        error("No vault result found for this file.")
        wait_for_enter()
        return

    encrypted_path = case_folder / f"{input_file.name}.enc"
    key_path = case_folder / f"{input_file.stem}.key"
    decrypted_path = case_folder / f"{input_file.stem}.dec"

    if not encrypted_path.is_file():
        error("Encrypted file not found.")
        wait_for_enter()
        return

    if not key_path.is_file():
        error("Encryption key not found.")
        wait_for_enter()
        return

    try:
        animated_status("Loading encryption key")

        key = load_key(str(key_path))

        animated_status("Decrypting file")

        decrypt_file(
            str(encrypted_path),
            str(decrypted_path),
            key,
        )

    except Exception as error:
        print(
            f"\n{ERROR}{BOLD}[-]{RESET} "
            f"{WHITE}Decryption failed: {error}{RESET}"
        )

        wait_for_enter()
        return

    print()

    success("File decrypted successfully.")

    print()

    print(
        f"{PRIMARY}{BOLD}"
        "  VAULT OUTPUT"
        f"{RESET}"
    )

    print(
        f"  {GRAY}Result folder{RESET}"
        f"   : {WHITE}{case_folder.name}{RESET}"
    )

    print(
        f"  {GRAY}Decrypted file{RESET}"
        f"  : {WHITE}{decrypted_path.name}{RESET}"
    )

    wait_for_enter()


# ============================================================
# HASH
# ============================================================

def calculate_hash_flow() -> None:
    clear_screen()
    show_banner()

    section_title("CALCULATE FILE HASH")

    input_file = get_input_file()

    if input_file is None:
        wait_for_enter()
        return

    print()

    animated_status("Calculating SHA-256")

    file_hash = calculate_file_hash(str(input_file))

    case_folder = find_latest_case_folder(input_file.name)

    if case_folder is None:
        case_folder = create_case_folder(input_file.name)

    hash_path = case_folder / f"{input_file.stem}.sha256"

    with open(hash_path, "w", encoding="utf-8") as file:
        file.write(file_hash)

    print()

    print(
        f"{GRAY}Algorithm{RESET}: "
        f"{WHITE}SHA-256{RESET}"
    )

    print()

    print(
        f"{GRAY}{file_hash}{RESET}"
    )

    print()

    success("Hash saved successfully.")

    print(
        f"{GRAY}Hash file{RESET}: "
        f"{WHITE}{hash_path.name}{RESET}"
    )

    wait_for_enter()


# ============================================================
# VERIFY INTEGRITY
# ============================================================

def verify_integrity_flow() -> None:
    clear_screen()
    show_banner()

    section_title("VERIFY FILE INTEGRITY")

    input_file = get_input_file()

    if input_file is None:
        wait_for_enter()
        return

    case_folder = find_latest_case_folder(input_file.name)

    if case_folder is None:
        error("No vault result found for this file.")
        warning("Calculate its hash first.")
        wait_for_enter()
        return

    hash_path = case_folder / f"{input_file.stem}.sha256"

    if not hash_path.is_file():
        error("SHA-256 hash file not found.")
        warning("Calculate the file hash first.")
        wait_for_enter()
        return

    with open(hash_path, "r", encoding="utf-8") as file:
        expected_hash = file.read().strip()

    print()

    animated_status("Verifying file integrity")

    verified = verify_file_integrity(
        str(input_file),
        expected_hash,
    )

    print()

    if verified:
        success("File Integrity Verified")
    else:
        error("File integrity check failed.")
        warning("The file has been modified.")

    wait_for_enter()


# ============================================================
# MAIN RUN LOOP
# ============================================================

def run():
    ensure_directories_exist()

    try:
        while True:
            clear_screen()

            show_banner()

            show_menu()

            choice = get_menu_choice()

            if choice == "0":
                print()
                info("Goodbye!")
                break

            elif choice == "1":
                encrypt_file_flow()

            elif choice == "2":
                decrypt_file_flow()

            elif choice == "3":
                calculate_hash_flow()

            elif choice == "4":
                verify_integrity_flow()

            else:
                print()
                error("Invalid option.")

                time.sleep(0.6)

            print()

    except KeyboardInterrupt:
        print()
        print()
        warning("Operation cancelled. Goodbye!")