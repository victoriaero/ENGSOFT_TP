# app/routers/samples.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.deps import get_db_session

router = APIRouter(prefix="/samples", tags=["samples"])

@router.post("/", response_model=schemas.SampleRead, status_code=status.HTTP_201_CREATED)
def create_sample(
    sample: schemas.SampleBase,
    db: Session = Depends(get_db_session)
) -> schemas.SampleRead:
    return crud.create_sample(db, sample)

@router.get("/by_dataset/{dataset_id}", response_model=List[schemas.SampleRead])
def list_samples(
    dataset_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db_session)
) -> List[schemas.SampleRead]:
    # Primeiro, tenta buscar as samples existentes
    samples = crud.get_samples(db, dataset_id, skip, limit)


    if not samples:
        # Se não houver, gera automaticamente conforme o dataset
        ds = crud.get_dataset(db, dataset_id)
        if not ds:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
        # cria cada Sample e suas SampleRows
        for i in range(ds.num_samples):
            s = crud.create_sample(db, schemas.SampleBase(
                dataset_id=dataset_id,
                sample_number=i + 1
            ))
            for idx in range(ds.sample_size):
                crud.create_sample_row(db, schemas.SampleRowBase(
                    sample_id=s.id,
                    dataset_id=dataset_id,
                    row_index=idx
                ))
        # busca de volta
        samples = crud.get_samples(db, dataset_id, skip, limit)
    return samples

@router.put("/{sample_id}/complete", response_model=schemas.SampleRead)
def complete_sample(
    sample_id: int,
    db: Session = Depends(get_db_session)
) -> schemas.SampleRead:
    completed = crud.mark_sample_completed(db, sample_id)
    if not completed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found")
    return completed

@router.get("/{sample_id}", response_model=schemas.SampleRead)
def get_sample(
    sample_id: int,
    db: Session = Depends(get_db_session)
) -> schemas.SampleRead:
    db_sample = crud.get_sample(db, sample_id)
    if not db_sample:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found")
    return db_sample

@router.delete("/{sample_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sample(
    sample_id: int,
    db: Session = Depends(get_db_session)
):
    deleted = crud.delete_sample(db, sample_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found")
    return

@router.get("/progress/{dataset_id}")
def get_dataset_progress(
    dataset_id: int,
    db: Session = Depends(get_db_session)
):
    samples = crud.get_samples(db, dataset_id)
    if not samples:
        raise HTTPException(404, "No samples found for dataset")

    total = len(samples)
    completed = sum(1 for s in samples if s.is_completed)

    return {"completed": completed, "total": total}


@router.get("/incomplete/by_dataset/{dataset_id}", response_model=List[schemas.SampleRead])
def list_incomplete_samples(
    dataset_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db_session)
) -> List[schemas.SampleRead]:
    # Primeiro, tenta buscar as samples existentes
    samples = [
        s for s in crud.get_samples(db, dataset_id, skip, limit)
        if not s.is_completed
    ]



    if not samples:
        # Se não houver, gera automaticamente conforme o dataset
        ds = crud.get_dataset(db, dataset_id)
        if not ds:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
        # cria cada Sample e suas SampleRows
        for i in range(ds.num_samples):
            s = crud.create_sample(db, schemas.SampleBase(
                dataset_id=dataset_id,
                sample_number=i + 1
            ))
            for idx in range(ds.sample_size):
                crud.create_sample_row(db, schemas.SampleRowBase(
                    sample_id=s.id,
                    dataset_id=dataset_id,
                    row_index=idx
                ))
        # busca de volta
        samples = crud.get_samples(db, dataset_id, skip, limit)
    return samples
