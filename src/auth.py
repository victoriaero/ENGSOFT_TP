import bcrypt
from src.connect import Database

class AuthManager:
    def __init__(self, db: Database):
        self.db = db

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed.encode())

    def register_user(self, username: str, password: str, role: str):
        if role not in ('dev', 'labeler'):
            raise ValueError("Role inválida: use 'dev' ou 'labeler'.")

        conn = self.db.connect()
        cursor = conn.cursor()

        try:
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            conn.commit()
            print(f"Usuário '{username}' cadastrado com sucesso como '{role}'.")
        except sqlite3.IntegrityError:
            print(f"Erro: o usuário '{username}' já existe.")
        finally:
            conn.close()

    def login(self, username: str, password: str):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id, password_hash, role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            user_id, password_hash, role = result
            if self.verify_password(password, password_hash):
                print(f"Login bem-sucedido! Usuário: {username}, Papel: {role}")
                return {"id": user_id, "username": username, "role": role}
            else:
                print("Senha incorreta.")
        else:
            print("Usuário não encontrado.")

        return None
