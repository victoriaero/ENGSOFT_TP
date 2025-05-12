from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.deps import get_db_session

router = APIRouter(prefix="/dataset_attributes", tags=["dataset_attributes"])

@router.post("/", response_model=schemas.DatasetAttributeRead, status_code=status.HTTP_201_CREATED)
def create_attribute(
    attribute: schemas.DatasetAttributeCreate,
    db: Session = Depends(get_db_session)
) -> schemas.DatasetAttributeRead:
    return crud.create_dataset_attribute(db, attribute)

@router.get("/", response_model=List[schemas.DatasetAttributeRead])
def list_attributes(
    dataset_id: int,
    db: Session = Depends(get_db_session)
) -> List[schemas.DatasetAttributeRead]:
    return crud.get_dataset_attributes(db, dataset_id)

@router.delete("/{attribute_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attribute(
    attribute_id: int,
    db: Session = Depends(get_db_session)
):
    deleted = crud.delete_dataset_attribute(db, attribute_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attribute not found")
    return
