from sqlalchemy.orm import Session,joinedload
from typing import List, Optional, Union
from app import models, schemas


# ------------------- Evaluator -------------------
def get_evaluator(db: Session, email: str) -> Optional[models.Evaluator]:
    return db.query(models.Evaluator).filter(models.Evaluator.email == email).first()

def get_evaluators(db: Session, skip: int = 0, limit: int = 100) -> List[models.Evaluator]:
    return db.query(models.Evaluator).offset(skip).limit(limit).all()

def create_evaluator(db: Session, evaluator: schemas.EvaluatorBase) -> models.Evaluator:
    db_obj = models.Evaluator(email=evaluator.email)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# ------------------- Dataset -------------------
def get_dataset(db: Session, dataset_id: int) -> Optional[models.Dataset]:
    return db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()

def get_datasets(db: Session, skip: int = 0, limit: int = 100) -> List[models.Dataset]:
    return db.query(models.Dataset).offset(skip).limit(limit).all()

def create_dataset(db: Session, dataset: schemas.DatasetCreate) -> models.Dataset:
    data = dataset.model_dump()
    db_obj = models.Dataset(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

from typing import Union

def update_dataset(
    db: Session,
    dataset_id: int,
    update_data: Union[schemas.DatasetCreate, schemas.DatasetUpdate]
):
    ds = db.query(models.Dataset).get(dataset_id)
    if not ds:
        return None
    patch = update_data.model_dump(exclude_unset=True)
    for key, value in patch.items():
        setattr(ds, key, value)
    db.commit()
    db.refresh(ds)
    return ds


def delete_dataset(db: Session, dataset_id: int) -> Optional[models.Dataset]:
    db_obj = get_dataset(db, dataset_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj

# ------------------- Dataset Attribute -------------------
def get_dataset_attribute(db: Session, attribute_id: int) -> Optional[models.DatasetAttribute]:
    return db.query(models.DatasetAttribute).filter(models.DatasetAttribute.id == attribute_id).first()

def get_dataset_attributes(db: Session, dataset_id: int) -> List[models.DatasetAttribute]:
    return db.query(models.DatasetAttribute).filter(models.DatasetAttribute.dataset_id == dataset_id).all()

def create_dataset_attribute(db: Session, attribute: schemas.DatasetAttributeCreate) -> models.DatasetAttribute:
    db_obj = models.DatasetAttribute(**attribute.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_dataset_attribute(db: Session, attribute_id: int) -> Optional[models.DatasetAttribute]:
    db_obj = get_dataset_attribute(db, attribute_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj

# ------------------- Dataset Label -------------------
def get_dataset_label(db: Session, label_id: int) -> Optional[models.DatasetLabel]:
    return db.query(models.DatasetLabel).filter(models.DatasetLabel.id == label_id).first()

def get_dataset_labels(db: Session, dataset_id: int) -> List[models.DatasetLabel]:
    return db.query(models.DatasetLabel).filter(models.DatasetLabel.dataset_id == dataset_id).all()

def create_dataset_label(db: Session, label: schemas.DatasetLabelCreate) -> models.DatasetLabel:
    db_obj = models.DatasetLabel(**label.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_dataset_label(db: Session, label_id: int) -> Optional[models.DatasetLabel]:
    db_obj = get_dataset_label(db, label_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj

# ------------------- Sample -------------------
def get_sample(db: Session, sample_id: int) -> Optional[models.Sample]:
    return db.query(models.Sample).filter(models.Sample.id == sample_id).first()

def get_samples(db: Session, dataset_id: int, skip: int = 0, limit: int = 100) -> List[models.Sample]:
    return db.query(models.Sample).filter(models.Sample.dataset_id == dataset_id).offset(skip).limit(limit).all()

def create_sample(db: Session, sample: schemas.SampleBase) -> models.Sample:
    db_obj = models.Sample(**sample.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def mark_sample_completed(db: Session, sample_id: int):
    from sqlalchemy import distinct

    sample = (
        db.query(models.Sample)
        .options(joinedload(models.Sample.dataset))
        .filter(models.Sample.id == sample_id)
        .first()
    )
    if not sample:
        return None

    dataset = sample.dataset
    required_evaluators = dataset.num_evaluators

    # todas as linhas da sample
    expected_rows = db.query(models.SampleRow.row_index).filter(
        models.SampleRow.sample_id == sample_id
    ).all()
    expected_row_indices = set(row[0] for row in expected_rows)

    if not expected_row_indices:
        return sample  # nada a fazer

    # todas as anotações agrupadas por avaliador
    annotations = db.query(
        models.Annotation.evaluator_email,
        models.Annotation.row_index
    ).filter(
        models.Annotation.sample_id == sample_id
    ).all()

    # agrupamos as anotações por avaliador
    from collections import defaultdict
    ann_by_evaluator = defaultdict(set)
    for email, row_index in annotations:
        ann_by_evaluator[email].add(row_index)

    # contamos quantos avaliadores cobriram todas as linhas da sample
    qualified_count = sum(
        1 for rows in ann_by_evaluator.values()
        if expected_row_indices.issubset(rows)
    )

    if qualified_count >= required_evaluators:
        sample.is_completed = True
        db.commit()
        db.refresh(sample)

    return sample



def delete_sample(db: Session, sample_id: int) -> Optional[models.Sample]:
    db_obj = get_sample(db, sample_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj

# ------------------- Sample Row -------------------
def get_sample_rows(db: Session, sample_id: int) -> List[models.SampleRow]:
    return db.query(models.SampleRow).filter(models.SampleRow.sample_id == sample_id).all()

def create_sample_row(db: Session, sample_row: schemas.SampleRowBase) -> models.SampleRow:
    db_obj = models.SampleRow(**sample_row.dict())
    db.add(db_obj)
    db.commit()
    return db_obj

def delete_sample_row(db: Session, sample_id: int, row_index: int) -> Optional[models.SampleRow]:
    db_obj = db.query(models.SampleRow).filter(
        models.SampleRow.sample_id == sample_id,
        models.SampleRow.row_index == row_index
    ).first()
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj

# ------------------- Annotation -------------------

def get_annotation(db: Session, annotation_id: int) -> Optional[models.Annotation]:
    return db.query(models.Annotation).filter(models.Annotation.id == annotation_id).first()

def get_annotations_by_sample(db: Session, sample_id: int) -> List[models.Annotation]:
    return db.query(models.Annotation).filter(models.Annotation.sample_id == sample_id).all()

def get_annotations_by_evaluator(db: Session, evaluator_email: str) -> List[models.Annotation]:
    return db.query(models.Annotation).filter(models.Annotation.evaluator_email == evaluator_email).all()

def create_annotation(db: Session, annotation_in: schemas.AnnotationCreate) -> models.Annotation:
    data = annotation_in.model_dump()
    db_obj = models.Annotation(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_annotation(db: Session, annotation_id: int) -> bool:
    ann = get_annotation(db, annotation_id)
    if not ann:
        return False
    db.delete(ann)
    db.commit()
    return True


def get_dataset_attributes(db: Session, dataset_id: int) -> list[models.DatasetAttribute]:
    """
    Retorna todos os DatasetAttribute associados a um dataset.
    """
    return (
        db.query(models.DatasetAttribute)
          .filter(models.DatasetAttribute.dataset_id == dataset_id)
          .order_by(models.DatasetAttribute.id)
          .all()
    )

