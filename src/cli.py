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


def run():

    while True:

        show_menu()

        choice = get_menu_choice()

        if choice == "0":
            print("Goodbye!")
            break

        elif choice == "1":
            print("Encrypt File selected.")

        elif choice == "2":
            print("Decrypt File selected.")

        elif choice == "3":
            print("Calculate Hash selected.")

        elif choice == "4":
            print("Verify Integrity selected.")

        else:
            print("Invalid option.")

        print()