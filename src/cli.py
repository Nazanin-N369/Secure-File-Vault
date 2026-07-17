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


from src.file_encryptor import (
    generate_key,
    encrypt_file,
)

from src.key_manager import save_key


def encrypt_file_flow():

    print("\n=== Encrypt File ===")

    print("\nEnter the path of the file you want to encrypt.")
    print("Example: C:\\Users\\Name\\Desktop\\secret.txt")

    input_path = input("\nInput file path: ").strip()


    print("\nEnter the output encrypted file name.")
    print("Example: secret.enc")

    output_path = input("\nEncrypted file path: ").strip()

    key = generate_key()

    encrypt_file(
        input_path,
        output_path,
        key,
    )

    save = input(
    "\nDo you want to save the encryption key? (Y/N): "
).strip().upper()
    if save == "Y":

        print("\nThe key file is required later to decrypt your file.")
        print("Example: secret.key")

        key_path = input(
            "\nEncryption key file path: "
        ).strip()

        save_key(
            key,
            key_path,
        )

        print("\nEncryption key saved.")

    print("\nFile encrypted successfully.")



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
            print("Decrypt File selected.")

        elif choice == "3":
            print("Calculate Hash selected.")

        elif choice == "4":
            print("Verify Integrity selected.")

        else:
            print("Invalid option.")

        print()