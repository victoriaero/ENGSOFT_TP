# app/routers/sample_rows.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from itertools import islice
from pathlib import Path
import csv

from app.deps import get_db_session
from app import crud, models
from app.schemas import SampleRowRead

router = APIRouter(prefix="/sample_rows", tags=["sample_rows"])

# mapeamento de tokens para separadores reais
SEP_CHARS = {
    "COMMA":     ",",
    "SEMICOLON": ";",
    "TAB":       "\t",
    "PIPE":      "|",
    "SPACE":     " ",
}


@router.get(
    "/by_sample/{sample_id}",
    response_model=List[int],
    summary="Lista índices de linhas de um sample"
)
def list_row_indices_by_sample(
    sample_id: int,
    db: Session = Depends(get_db_session)
) -> List[int]:
    """
    Retorna apenas a lista de row_index associados a um sample,
    sem carregar CSV algum.
    """
    sample = crud.get_sample(db, sample_id)
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")

    rows = (
        db.query(models.SampleRow)
          .filter(models.SampleRow.sample_id == sample_id)
          .order_by(models.SampleRow.row_index)
          .all()
    )

    return [r.row_index for r in rows]


@router.get(
    "/by_sample/{sample_id}/row/{row_index}",
    response_model=SampleRowRead,
    summary="Retorna dados de uma única linha filtrada pelos atributos"
)
def get_row_by_index(
    sample_id: int,
    row_index: int,
    db: Session = Depends(get_db_session)
) -> SampleRowRead:
    """
    Lê apenas a linha `row_index` do CSV do sample, filtra pelos atributos
    associados ao dataset e retorna um SampleRowRead.
    """
    # 1) Valida existência do sample e do dataset
    sample = crud.get_sample(db, sample_id)
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")

    dataset = crud.get_dataset(db, sample.dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # 2) Traduz token de separador
    sep = SEP_CHARS.get(dataset.separator)
    if sep is None:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid separator token: {dataset.separator}"
        )

    # 3) Busca os atributos permitidos para este dataset
    attrs = crud.get_dataset_attributes(db, dataset.id)
    allowed = {a.attr_name for a in attrs}

    # 4) Stream‐read até a linha desejada
    csv_path = Path(dataset.path).expanduser().resolve()
    try:
        with csv_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f, delimiter=sep)
            # pula até `row_index` e captura apenas essa linha
            row_dict = next(islice(reader, row_index, row_index + 1), None)
    except FileNotFoundError:
        raise HTTPException(
            status_code=400,
            detail=f"CSV file not found at path: {csv_path}"
        )

    if row_dict is None:
        raise HTTPException(status_code=404, detail="Row index out of bounds")

    # 5) Filtra só as colunas (keys) permitidas
    filtered: Dict[str, str] = {
        k: v for k, v in row_dict.items() if k in allowed
    }

    # 6) Retorna conforme o schema
    return SampleRowRead(
        sample_id=sample.id,
        dataset_id=dataset.id,
        row_index=row_index,
        data=filtered
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta uma linha de sample"
)
def delete_row(
    sample_id: int,
    row_index: int,
    db: Session = Depends(get_db_session)
):
    """
    Deleta o registro de SampleRow(sample_id, row_index) no banco.
    """
    deleted = crud.delete_sample_row(db, sample_id, row_index)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sample row not found"
        )
    return
