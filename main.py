from src.auth import AuthManager
from src.connect import Database

def menu():
    print("\n--- MENU ---")
    print("1. Registrar usuário")
    print("2. Login")
    print("0. Sair")

def main():
    db = Database()
    auth = AuthManager(db)

    while True:
        menu()
        choice = input("Escolha uma opção: ")

        if choice == "1":
            username = input("Usuário: ")
            password = input("Senha: ")
            role = input("Papel ('dev' ou 'labeler'): ")
            auth.register_user(username, password, role)

        elif choice == "2":
            username = input("Usuário: ")
            password = input("Senha: ")
            auth.login(username, password)

        elif choice == "0":
            print("Encerrando.")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
