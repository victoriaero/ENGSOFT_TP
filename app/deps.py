from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db


def get_db_session(db: Session = Depends(get_db)) -> Session:
    """
    Retorna a sessão do banco de dados para injeção nas rotas
    """
    return db
