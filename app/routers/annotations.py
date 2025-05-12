# app/routers/annotations.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app import crud, schemas, models
from app.deps import get_db_session

router = APIRouter(prefix="/annotations", tags=["annotations"])

@router.post("/", response_model=schemas.AnnotationRead, status_code=status.HTTP_201_CREATED)
def create_annotation(
    annotation: schemas.AnnotationCreate,
    db: Session = Depends(get_db_session)
) -> schemas.AnnotationRead:
    return crud.create_annotation(db, annotation)

@router.get(
    "/by_sample/{sample_id}",
    response_model=List[schemas.AnnotationRead],
    summary="Lista as anotações de uma sample, opcionalmente filtrando por avaliador"
)
def list_annotations_by_sample(
    sample_id: int,
    evaluator_email: Optional[str] = Query(
        None,
        alias="evaluator_email",
        description="Filtro opcional para retornar apenas anotações deste evaluator"
    ),
    db: Session = Depends(get_db_session)
) -> List[schemas.AnnotationRead]:
    # monta a query base
    query = db.query(models.Annotation).filter(models.Annotation.sample_id == sample_id)

    # aplica filtro por evaluator_email, se informado
    if evaluator_email:
        query = query.filter(models.Annotation.evaluator_email == evaluator_email)

    results = query.all()
    return results

@router.get("/by_evaluator/{evaluator_email}", response_model=List[schemas.AnnotationRead])
def list_annotations_by_evaluator(
    evaluator_email: str,
    db: Session = Depends(get_db_session)
) -> List[schemas.AnnotationRead]:
    return crud.get_annotations_by_evaluator(db, evaluator_email)

@router.delete("/{annotation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_annotation(
    annotation_id: int,
    db: Session = Depends(get_db_session)
):
    deleted = crud.delete_annotation(db, annotation_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Annotation not found")
    return

@router.delete(
    "/by_sample/{sample_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Apaga todas as anotações de uma sample para um evaluator"
)
def delete_annotations_by_sample(
    sample_id: int,
    evaluator_email: str = Query(..., alias="evaluator_email"),
    db: Session = Depends(get_db_session)
):
    # Remove tudo de uma vez
    db.query(models.Annotation) \
      .filter(
        models.Annotation.sample_id == sample_id,
        models.Annotation.evaluator_email == evaluator_email
      ) \
      .delete(synchronize_session=False)
    db.commit()
    return
