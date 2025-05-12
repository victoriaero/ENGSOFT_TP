from pydantic import BaseModel
from fastapi import (
    APIRouter, Depends, HTTPException,
Body, status, Query)

from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload

from collections import defaultdict
from typing import List, Dict
from pathlib import Path
import random
import csv
import io

from app import crud, schemas, models
from app.deps import get_db_session

router = APIRouter(prefix="/datasets", tags=["datasets"])

# ------------------------ helpers ------------------------
SEP_MAP = {",": "COMMA", ";": "SEMICOLON", "\t": "TAB", "|": "PIPE", " ": "SPACE"}
SEP_CHARS = {
    "COMMA": ",", "SEMICOLON": ";", "TAB": "\t", "PIPE": "|", "SPACE": " "
}


# ---------------------- CRUD manual ----------------------
@router.post("/", response_model=schemas.DatasetRead, status_code=201)
def create_dataset(
    dataset: schemas.DatasetCreate, db: Session = Depends(get_db_session)
) -> schemas.DatasetRead:
    data = dataset.model_dump()          # <- model_dump()
    sep = data.get("separator")
    if sep:
        if sep in SEP_MAP:
            data["separator"] = SEP_MAP[sep]
        elif sep not in SEP_MAP.values():
            raise HTTPException(400, "Invalid separator.")
    return crud.create_dataset(db, schemas.DatasetCreate(**data))

@router.get("/", response_model=List[schemas.DatasetRead])
def list_datasets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db_session)
) -> List[schemas.DatasetRead]:
    return (
        db.query(models.Dataset)
          .options(
              joinedload(models.Dataset.attributes),
              joinedload(models.Dataset.labels),
          )
          .offset(skip)
          .limit(limit)
          .all()
    )

@router.get("/{dataset_id}", response_model=schemas.DatasetRead)
def get_dataset(
    dataset_id: int,
    db: Session = Depends(get_db_session)
) -> schemas.DatasetRead:
    ds = (
        db.query(models.Dataset)
          .options(
              joinedload(models.Dataset.attributes),
              joinedload(models.Dataset.labels),
          )
          .filter(models.Dataset.id == dataset_id)
          .first()
    )
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return ds


@router.patch("/{dataset_id}", response_model=schemas.DatasetRead)
def update_dataset(
    dataset_id: int,
    dataset: schemas.DatasetUpdate,
    db: Session = Depends(get_db_session),
) -> schemas.DatasetRead:
    # converte só os campos que vieram no JSON
    data = dataset.model_dump(exclude_unset=True)

    # validação de separator (mesma lógica do POST/PUT original)
    sep = data.get("separator")
    if sep:
        if sep in SEP_MAP:
            data["separator"] = SEP_MAP[sep]
        elif sep not in SEP_MAP.values():
            raise HTTPException(status_code=400, detail="Invalid separator.")

    # aplica o patch no banco
    updated = crud.update_dataset(db, dataset_id, dataset)
    if not updated:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return updated



@router.delete("/{dataset_id}", status_code=204)
def delete_dataset(dataset_id: int, db: Session = Depends(get_db_session)) -> None:
    if not crud.delete_dataset(db, dataset_id):
        raise HTTPException(404, "Dataset not found")
    return

@router.post(
    "/{dataset_id}/verify-password",
    response_model=schemas.PasswordCheckResponse,
    summary="Check dataset password"
)
def verify_dataset_password(
    dataset_id: int,
    payload: schemas.PasswordCheck,       # { password: str }
    db: Session = Depends(get_db_session),
) -> schemas.PasswordCheckResponse:
    ds = crud.get_dataset(db, dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")

    if ds.access_pwd != payload.password:
        # retorna 200 com sucesso=false
        return schemas.PasswordCheckResponse(
            success=False,
            message="Wrong password"
        )

    return schemas.PasswordCheckResponse(
        success=True,
        message="Password correct"
    )

# ---------------------- Endpoint registro ----------------------

@router.post("/register", response_model=schemas.DatasetRead, status_code=201)
def register_dataset(
    payload: schemas.DatasetCreate = Body(...),
    db: Session = Depends(get_db_session),
) -> schemas.DatasetRead:

    csv_path = Path(payload.path).expanduser().resolve()
    if not csv_path.is_file():
        raise HTTPException(400, f"Arquivo não existe: {csv_path}")

    # ------------------------------------------------------------------
    # Detecta separador e cabeçalho lendo as primeiras linhas do arquivo
    # ------------------------------------------------------------------
    with csv_path.open("r", encoding="utf-8", errors="ignore") as f:
        preview = "".join([next(f) for _ in range(10)])
    try:
        sep_char = csv.Sniffer().sniff(preview).delimiter
    except csv.Error:
        sep_char = ","
    if sep_char not in SEP_MAP:
        raise HTTPException(400, f"Separador não suportado: '{sep_char}'")

    header = preview.splitlines()[0].split(sep_char)
    if not header:
        raise HTTPException(400, "Cabeçalho do CSV vazio")

    # ------------------------------------------------------------------
    # Conta linhas de dados (sem header) e valida quantidade necessária
    # ------------------------------------------------------------------
    with csv_path.open("r", encoding="utf-8", errors="ignore") as f:
        total_rows = sum(1 for _ in f) - 1

    required = payload.sample_size * payload.num_samples
    if required > total_rows:
        raise HTTPException(
            400,
            f"O arquivo possui {total_rows} instâncias de dados; o número informado pelo usuário (Samples x Número de Samples) totaliza {required} instâncias e excede o número de dados."
        )

    # ------------------------------------------------------------------
    # Monta o dicionário FINAL que será salvo (evitando duplicidades)
    # ------------------------------------------------------------------
    data = payload.model_dump()
    # força tipo csv e token de separador
    data["type"] = "csv"
    data["separator"] = SEP_MAP[sep_char]

    # ------------------------------------------------------------------
    # Cria o dataset (sem campos duplicados)
    # ------------------------------------------------------------------
    ds = crud.create_dataset(db, schemas.DatasetCreate(**data))

    # cria atributos do cabeçalho
    for col in header:
        crud.create_dataset_attribute(
            db, schemas.DatasetAttributeCreate(dataset_id=ds.id, attr_name=col)
        )

    # ------------------------------------------------------------------
    # Gera índices aleatórios *sem reposição* e monta samples/sample_rows
    # ------------------------------------------------------------------
    all_indices = list(range(total_rows))
    random.shuffle(all_indices)
    chosen = all_indices[:required]

    for i in range(payload.num_samples):
        sample = crud.create_sample(
            db,
            schemas.SampleBase(dataset_id=ds.id, sample_number=i + 1)
        )
        block = chosen[i * payload.sample_size:(i + 1) * payload.sample_size]
        for idx in block:
            crud.create_sample_row(
                db,
                schemas.SampleRowBase(
                    sample_id=sample.id,
                    dataset_id=ds.id,
                    row_index=idx
                ),
            )

    return ds

@router.get("/preview-attributes", response_model=List[str])
def preview_attributes(
    path: str = Query(..., description="Caminho do CSV")
):
    csv_path = Path(path).expanduser().resolve()
    if not csv_path.is_file():
        raise HTTPException(400, f"Arquivo não encontrado em: {csv_path}")

    # leia poucas linhas só pra extrair header
    with csv_path.open("r", encoding="utf-8", errors="ignore") as f:
        first = next(f, "")
    # descubra separador igual ao register…
    try:
        sep_char = csv.Sniffer().sniff(first).delimiter
    except csv.Error:
        sep_char = ","
    header = first.strip().split(sep_char)
    return header

@router.get("/{dataset_id}/attributes", response_model=List[str])
def list_dataset_attributes(
    dataset_id: int, db: Session = Depends(get_db_session)
):
    ds = crud.get_dataset(db, dataset_id)
    if not ds:
        raise HTTPException(404, "Dataset not found")
    return [attr.attr_name for attr in ds.attributes]

@router.post("/{dataset_id}/configure", response_model=schemas.DatasetRead)
def configure_dataset(
    dataset_id: int,
    cfg: schemas.DatasetConfigure,
    db: Session = Depends(get_db_session),
):
    ds = crud.get_dataset(db, dataset_id)
    if not ds:
        raise HTTPException(404, "Dataset not found")

    # -------- atributos --------
    if cfg.attributes:
        keep = set(cfg.attributes)
        for attr in crud.get_dataset_attributes(db, dataset_id):
            if attr.attr_name not in keep:
                crud.delete_dataset_attribute(db, attr.id)

    # -------- rótulos --------
    if cfg.labels:
        # elimina espaços vazios, remove duplicados
        new_labels = {lab.strip() for lab in cfg.labels if lab.strip()}
        for text in new_labels:
            crud.create_dataset_label(
                db,
                schemas.DatasetLabelCreate(dataset_id=dataset_id,
                                           label_text=text)
            )

    return ds

@router.get("/{dataset_id}/annotations/download")
def download_annotations_csv(
    dataset_id: int,
    db: Session = Depends(get_db_session)
):
    # 1) dataset + attrs + labels
    ds = (
        db.query(models.Dataset)
          .options(
              joinedload(models.Dataset.attributes),
              joinedload(models.Dataset.labels)
          )
          .filter(models.Dataset.id == dataset_id)
          .first()
    )
    if not ds:
        raise HTTPException(404, "Dataset not found")

    # 2) samples concluídas
    sample_ids = [
        s.id for s in db.query(models.Sample.id)
                       .filter(models.Sample.dataset_id == dataset_id,
                               models.Sample.is_completed == 1)
    ]
    if not sample_ids:
        raise HTTPException(404, "No completed samples")

    # 3) anotações dessas samples
    annotations = (
        db.query(models.Annotation, models.DatasetLabel.label_text)
          .join(models.DatasetLabel,
                models.Annotation.label_id == models.DatasetLabel.id)
          .filter(models.Annotation.sample_id.in_(sample_ids))
          .all()
    )

    # 4) row_index → set{labels}
    labels_by_row: Dict[int, set] = defaultdict(set)
    for ann, label_text in annotations:
        labels_by_row[ann.row_index].add(label_text)

    # 5) CSV original
    sep       = SEP_CHARS[ds.separator]
    csv_path  = Path(ds.path).expanduser()
    attr_cols = [a.attr_name for a in ds.attributes]
    label_cols = [lab.label_text for lab in ds.labels]  # pode ser 1 só

    header = attr_cols + label_cols

    def row_generator():
        with csv_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f, delimiter=sep)
            for idx, row in enumerate(reader):
                if idx in labels_by_row:
                    base = [row[c] for c in attr_cols]
                    flags = [
                        "1" if lab in labels_by_row[idx] else "0"
                        for lab in label_cols
                    ]
                    yield base + flags

    # 6) streaming response
    def stream():
        buf, writer = io.StringIO(), csv.writer(io.StringIO())
        writer = csv.writer(buf)
        writer.writerow(header)
        for r in row_generator():
            writer.writerow(r)
            yield buf.getvalue()
            buf.seek(0); buf.truncate(0)

    safe_name = ds.name.replace(" ", "_").replace("/", "_")
    headers = {
        "Content-Disposition": f'attachment; filename="{safe_name}_classification.csv"'
    }
    return StreamingResponse(stream(), media_type="text/csv", headers=headers)
