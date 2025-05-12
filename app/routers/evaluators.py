# app/routers/evaluators.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.deps import get_db_session

router = APIRouter(prefix="/evaluators", tags=["evaluators"])

@router.post("/", response_model=schemas.EvaluatorRead, status_code=status.HTTP_201_CREATED)
def create_evaluator(
    evaluator: schemas.EvaluatorBase,
    db: Session = Depends(get_db_session)
) -> schemas.EvaluatorRead:
    existing = crud.get_evaluator(db, evaluator.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Evaluator already exists")
    return crud.create_evaluator(db, evaluator)

@router.get("/", response_model=List[schemas.EvaluatorRead])
def list_evaluators(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db_session)
) -> List[schemas.EvaluatorRead]:
    return crud.get_evaluators(db, skip, limit)

@router.get("/{email}", response_model=schemas.EvaluatorRead)
def get_evaluator(
    email: str,
    db: Session = Depends(get_db_session)
) -> schemas.EvaluatorRead:
    db_eval = crud.get_evaluator(db, email)
    if not db_eval:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluator not found")
    return db_eval
