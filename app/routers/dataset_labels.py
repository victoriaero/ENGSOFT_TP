# app/routers/dataset_labels.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.deps import get_db_session


router = APIRouter(prefix="/dataset_labels", tags=["dataset_labels"])

@router.post("/", response_model=schemas.DatasetLabelRead, status_code=status.HTTP_201_CREATED)
def create_label(
    label: schemas.DatasetLabelCreate,
    db: Session = Depends(get_db_session)
) -> schemas.DatasetLabelRead:
    return crud.create_dataset_label(db, label)

@router.get("/", response_model=List[schemas.DatasetLabelRead])
def list_labels(
    dataset_id: int,
    db: Session = Depends(get_db_session)
) -> List[schemas.DatasetLabelRead]:
    return crud.get_dataset_labels(db, dataset_id)

@router.delete("/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_label(
    label_id: int,
    db: Session = Depends(get_db_session)
):
    deleted = crud.delete_dataset_label(db, label_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Label not found")
    return
