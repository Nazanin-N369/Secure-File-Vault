from pathlib import Path
from src.key_manager import (
    load_key,
    save_key,
)
from src.file_encryptor import decrypt_file
from src.file_hasher import calculate_file_hash
from src.integrity_checker import verify_file_integrity
from src.file_encryptor import (generate_key,encrypt_file,)
from src.paths import create_case_folder


def show_menu():
    
    print("=" * 40)
    print("Secure File Vault")
    print("=" * 40)

    print("1. Encrypt File")
    print("2. Decrypt File")
    print("3. Calculate File Hash")
    print("4. Verify File Integrity")
    print("0. Exit")


def get_menu_choice():

    return input("\nSelect an option: ").strip()




def ask_yes_no(message: str) -> bool:
    while True:
        answer = input(message).strip().upper()

        if answer in ("Y", "N"):
            return answer == "Y"

        print("Please enter Y or N.")

def encrypt_file_flow():

    print("\n=== Encrypt File ===")

    print("\nEnter the path of the file you want to encrypt.")
    print("Example: C:\\Users\\Name\\Desktop\\secret.txt")

    input_path = input("\nInput file path: ").strip()
    if not Path(input_path).exists():
        print("\n✗ File not found.")
        print("Please check the file path.")
        input("\nPress Enter to continue...")
        return


    # print("\nEnter the output encrypted file name.")
    # print("Example: secret.enc")

    # output_path = input("\nEncrypted file path: ").strip()
    # if not output_path:
    #     print("\nOutput file path cannot be empty.")
    #     input("\nPress Enter to continue...")
    #     return

    key = generate_key()
    
    case_folder = create_case_folder(input_path)

    original_name = Path(input_path).name
    base_name = Path(input_path).stem
    
    encrypt_file(
        input_path,
        key,
    )

    save = ask_yes_no(
    "\nDo you want to save the encryption key? (Y/N): "
)    
    if save :

        print("\nThe key file is required later to decrypt your file.")
        print("Example: secret.key")

        key_path = input(
            "\nEncryption key file name/path: "
        ).strip()

        save_key(
            key,
            key_path,
        )

        print("\nEncryption key saved.")

    print("\n✓ File encrypted successfully.")
    input("\nPress Enter to continue...")

def decrypt_file_flow():
    
    print("\n=== Decrypt File ===")

    print("\nEnter the encrypted file path.")
    encrypted_path = input("\nEncrypted file: ").strip()

    if not Path(encrypted_path).exists():
        print("\n✗ Encrypted file not found.")
        input("\nPress Enter to continue...")
        return

    print("\nEnter the output decrypted file path.")
    output_path = input("\nOutput file: ").strip()

    if not output_path:
        print("\nOutput path cannot be empty.")
        input("\nPress Enter to continue...")
        return

    print("\nEnter the encryption key file.")
    key_path = input("\nKey file: ").strip()

    if not Path(key_path).exists():
        print("\nKey file not found.")
        input("\nPress Enter to continue...")
        return

    key = load_key(key_path)

    decrypt_file(
        encrypted_path,
        output_path,
        key,
    )

    print("\n✓ File decrypted successfully.")
    input("\nPress Enter to continue...")

def calculate_hash_flow() -> None:
    
    print("\n" + "=" * 40)
    print("Calculate File Hash")
    print("=" * 40)

    print("\nEnter file path.")
    print("Example: C:\\Users\\User\\Desktop\\secret.pdf\n")

    file_path = input("File: ").strip()

    if not Path(file_path).exists():
        print("\n✗ File not found.")
        input("\nPress Enter to continue...")
        return

    print("\nCalculating SHA-256...\n")

    file_hash = calculate_file_hash(file_path)

    print("Algorithm: SHA-256\n")

    print(file_hash)

    save = ask_yes_no("\nSave hash to file? (Y/N): ")

    if save:

        hash_path = input(
            "\nHash file path (.txt): "
        ).strip()

        if not hash_path:
            print("Cancelled.")
            input("\nPress Enter to continue...")
            return

        with open(
            hash_path,
            "w",
            encoding="utf-8",
        ) as file:
            file.write(file_hash)

        print("\n✓ Hash saved successfully.")
        input("\nPress Enter to continue...")
           
def verify_integrity_flow() -> None:
    
    print("\n" + "=" * 40)
    print("Verify File Integrity")
    print("=" * 40)

    file_path = input("\nOriginal file: ").strip()

    if not Path(file_path).exists():
        print("\n✗ File not found.")
        input("\nPress Enter to continue...")
        return

    hash_path = input(
        "\nHash file: "
    ).strip()

    if not Path(hash_path).exists():
        print("\n✗ Hash file not found.")
        input("\nPress Enter to continue...")
        return

    with open(
    hash_path,
    "r",
    encoding="utf-8",) as file:
        expected_hash = file.read().strip()

    print("\nVerifying...\n")

    verified = verify_file_integrity(
        file_path,
        expected_hash,
    )

    if verified:

        print("✓ File Integrity Verified")
        input("\nPress Enter to continue...")

    else:

        print("✗ File integrity check failed.")
        print("File has been modified.")
        

def run():

    while True:

        show_menu()

        choice = get_menu_choice()

        if choice == "0":
            print("Goodbye!")
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
            print("Invalid option.")

        print()