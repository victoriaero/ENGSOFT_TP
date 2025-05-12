import os
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext

# --- Configuração de hashing e arquivo de senha ---
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/auth", tags=["auth"])

PASS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "db", "admin_password.txt"
)

def read_hash() -> str:
    """
    Lê o hash bcrypt gravado em db/admin_password.txt.
    Deve existir e conter apenas o hash.
    """
    try:
        with open(PASS_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Arquivo de senha não encontrado. Inicialize o hash primeiro."
        )

def write_hash(new_hash: str) -> None:
    """
    Sobrescreve db/admin_password.txt com o novo hash bcrypt.
    """
    with open(PASS_FILE, "w") as f:
        f.write(new_hash)

# --- Modelos de request ---
class LoginRequest(BaseModel):
    password: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

# --- Endpoints ---

@router.post("/login", summary="Verifica a senha admin")
def login(req: LoginRequest):
    """
    Recebe {"password": "..."} e retorna {"success": True} se bater com o hash.
    Caso contrário, 401 Unauthorized.
    """
    current_hash = read_hash()
    if not pwd_ctx.verify(req.password, current_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha incorreta"
        )
    return {"success": True}

@router.post("/change-password", summary="Altera a senha admin")
def change_password(req: ChangePasswordRequest):
    """
    Recebe {"old_password": "...", "new_password": "..."}.
    Se old_password bater com o hash atual, gera hash de new_password,
    grava em admin_password.txt e retorna {"success": True}.
    Caso contrário, 400 Bad Request.
    """
    current_hash = read_hash()
    if not pwd_ctx.verify(req.old_password, current_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha atual incorreta"
        )

    new_hash = pwd_ctx.hash(req.new_password)
    write_hash(new_hash)
    return {"success": True}
