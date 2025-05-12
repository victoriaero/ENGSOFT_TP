from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Dict, List, Optional, Any

# ------------------- Evaluator -------------------
class EvaluatorBase(BaseModel):
    email: EmailStr

class EvaluatorRead(EvaluatorBase):
    created_at: datetime

    class Config:
        orm_mode = True

# ------------------- Dataset -------------------
class DatasetBase(BaseModel):
    name: str = Field(..., max_length=100)
    path: str 
    owner_name: Optional[str] = Field(default=None)
    description: str
    type: str
    separator: Optional[str] = Field(default=None)
    sample_size: int = Field(..., gt=0, description="Number of rows per sample, must be > 0")
    num_samples: int = Field(..., gt=0, description="Total number of samples, must be > 0")
    num_evaluators: int = Field(..., gt=0, description="Number of evaluators per sample, must be > 0")
    is_multilabel: bool = False
    is_private: bool = False

class DatasetCreate(DatasetBase):
    path: str
    access_pwd: Optional[str] = None

class DatasetRead(DatasetBase):
    id: int
    owner_name: Optional[str]
    access_pwd: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

class PasswordCheck(BaseModel):
    password: str

class PasswordCheckResponse(BaseModel):
    success: bool
    message: Optional[str] = None

    class Config:
        orm_mode = True

class DatasetUpdate(BaseModel):
    name: Optional[str]         = None
    owner_name: Optional[str]   = None
    description: Optional[str]  = None
    access_pwd: Optional[str]   = None


# ------------------- Dataset Attribute -------------------
class DatasetAttributeBase(BaseModel):
    dataset_id: int
    attr_name: str

class DatasetAttributeCreate(DatasetAttributeBase):
    pass

class DatasetAttributeRead(DatasetAttributeBase):
    id: int

    class Config:
        orm_mode = True

# ------------------- Dataset Label -------------------
class DatasetLabelBase(BaseModel):
    dataset_id: int
    label_text: str

class DatasetLabelCreate(DatasetLabelBase):
    pass

class DatasetLabelRead(DatasetLabelBase):
    id: int

    class Config:
        orm_mode = True

# ------------------- Sample -------------------
class SampleBase(BaseModel):
    dataset_id: int
    sample_number: int

class SampleRead(SampleBase):
    id: int
    is_completed: bool
    created_at: datetime

    class Config:
        orm_mode = True

# ------------------- SampleRow -------------------
class SampleRowBase(BaseModel):
    sample_id: int
    dataset_id: int
    row_index: int

# Novo: o payload de leitura inclui um dict com os dados
class SampleRowRead(SampleRowBase):
    data: Dict[str, Any]

    class Config:
        orm_mode = True

# ------------------- Annotation -------------------
class AnnotationBase(BaseModel):
    sample_id: int
    row_index: int
    evaluator_email: EmailStr
    label_id: int

class AnnotationCreate(AnnotationBase):
    pass

class AnnotationRead(AnnotationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# -------------------- Others -------------------

class DatasetRead(DatasetBase):
    id: int
    owner_name: Optional[str]
    access_pwd: Optional[str]
    created_at: datetime

    # NOVO: listas aninhadas
    attributes: List[DatasetAttributeRead]
    labels:     List[DatasetLabelRead]

    class Config:
        orm_mode = True

class DatasetConfigure(BaseModel):
    attributes: Optional[List[str]] = None   # atributos a manter
    labels: Optional[List[str]] = None       # rótulos separados

class DatasetDetails(BaseModel):
    id: int
    name: str
    owner_name: str | None = None
    path: str | None = None             # <- aqui
    description: str | None = None
    type: str
    sample_size: int
    num_samples: int
    num_evaluators: int
    is_multilabel: bool
    is_private: bool
    attributes: list[DatasetAttributeRead] = []
    labels: list[DatasetLabelRead] = []
