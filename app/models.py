from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Text,
    func
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# ---------- Evaluator ----------
class Evaluator(Base):
    __tablename__ = "evaluators"

    email = Column(String(255), primary_key=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    annotations = relationship("Annotation", back_populates="evaluator")

# ---------- Dataset ----------
class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    path = Column(String(255), nullable=False) 
    owner_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False, default="")           # NOVO!
    type = Column(Text, nullable=False)
    separator = Column(Text)
    sample_size = Column(Integer, nullable=False)
    num_samples = Column(Integer, nullable=False)
    num_evaluators = Column(Integer, nullable=False)
    is_multilabel = Column(Boolean, nullable=False, default=False)
    is_private = Column(Boolean, nullable=False, default=False)
    access_pwd = Column(String(255))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    attributes = relationship("DatasetAttribute", back_populates="dataset",
                              cascade="all, delete-orphan")
    labels = relationship("DatasetLabel", back_populates="dataset",
                          cascade="all, delete-orphan")
    samples = relationship("Sample", back_populates="dataset",
                           cascade="all, delete-orphan")
    sample_rows = relationship("SampleRow", back_populates="dataset",
                               cascade="all, delete-orphan")

# ---------- DatasetAttribute ----------
class DatasetAttribute(Base):
    __tablename__ = "dataset_attributes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    attr_name = Column(String, nullable=False)

    dataset = relationship("Dataset", back_populates="attributes")

# ---------- DatasetLabel ----------
class DatasetLabel(Base):
    __tablename__ = "dataset_labels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    label_text = Column(String, nullable=False)

    dataset = relationship("Dataset", back_populates="labels")
    annotations = relationship("Annotation", back_populates="label",
                               cascade="all, delete-orphan")

# ---------- Sample ----------
class Sample(Base):
    __tablename__ = "samples"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    sample_number = Column(Integer, nullable=False)
    is_completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    dataset = relationship("Dataset", back_populates="samples")
    sample_rows = relationship("SampleRow", back_populates="sample",
                               cascade="all, delete-orphan")
    annotations = relationship("Annotation", back_populates="sample",
                               cascade="all, delete-orphan")

# ---------- SampleRow ----------
class SampleRow(Base):
    __tablename__ = "sample_rows"

    sample_id = Column(Integer, ForeignKey("samples.id"), primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), primary_key=True)
    row_index = Column(Integer, primary_key=True, nullable=False)

    sample = relationship("Sample", back_populates="sample_rows")
    dataset = relationship("Dataset", back_populates="sample_rows")

# ---------- Annotation ----------
class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    row_index = Column(Integer, nullable=False)
    evaluator_email = Column(String(255), ForeignKey("evaluators.email"), nullable=False)
    label_id = Column(Integer, ForeignKey("dataset_labels.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    sample = relationship("Sample", back_populates="annotations")
    evaluator = relationship("Evaluator", back_populates="annotations")
    label = relationship("DatasetLabel", back_populates="annotations")
