PRAGMA foreign_keys = ON;

-- 1) evaluators
CREATE TABLE evaluators (
  email       VARCHAR(255) PRIMARY KEY NOT NULL,
  created_at  DATETIME      DEFAULT CURRENT_TIMESTAMP
);

-- 2) datasets
CREATE TABLE datasets (
  id               INTEGER PRIMARY KEY AUTOINCREMENT,
  name             VARCHAR(100)   NOT NULL,
  path             VARCHAR(255)   NOT NULL,
  owner_name       VARCHAR(100),
  description      TEXT           NOT NULL,
  type             TEXT           NOT NULL CHECK(type IN ('csv','jsonl')),
  separator        TEXT           CHECK(separator IN ('COMMA','SEMICOLON','TAB','PIPE','SPACE')),
  sample_size      INTEGER        NOT NULL CHECK(sample_size > 0),
  num_samples      INTEGER        NOT NULL CHECK(num_samples > 0),
  num_evaluators   INTEGER        NOT NULL CHECK(num_evaluators > 0),
  is_multilabel    INTEGER        NOT NULL DEFAULT 0,  -- 0=false, 1=true
  is_private       INTEGER        NOT NULL DEFAULT 0,
  access_pwd       VARCHAR(255),
  created_at       DATETIME       DEFAULT CURRENT_TIMESTAMP,
  -- validação de senha se privado
  CHECK (is_private = 0 
         OR (access_pwd IS NOT NULL AND access_pwd <> ''))
);

-- 3) dataset_attributes
CREATE TABLE dataset_attributes (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  dataset_id INTEGER NOT NULL,
  attr_name  VARCHAR(255) NOT NULL,
  FOREIGN KEY(dataset_id) REFERENCES datasets(id) ON DELETE CASCADE
);

-- 4) dataset_labels
CREATE TABLE dataset_labels (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  dataset_id INTEGER NOT NULL,
  label_text VARCHAR(255) NOT NULL,
  FOREIGN KEY(dataset_id) REFERENCES datasets(id) ON DELETE CASCADE,
  UNIQUE(dataset_id, label_text)
);

-- 5) samples
CREATE TABLE samples (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  dataset_id     INTEGER NOT NULL,
  sample_number  INTEGER NOT NULL,
  is_completed   INTEGER NOT NULL DEFAULT 0,
  created_at     DATETIME  DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(dataset_id) REFERENCES datasets(id) ON DELETE CASCADE,
  UNIQUE(dataset_id, sample_number)
);

-- 6) sample_rows
CREATE TABLE sample_rows (
  sample_id  INTEGER NOT NULL,
  dataset_id INTEGER NOT NULL,
  row_index  INTEGER NOT NULL,
  FOREIGN KEY(sample_id)  REFERENCES samples(id)  ON DELETE CASCADE,
  FOREIGN KEY(dataset_id) REFERENCES datasets(id) ON DELETE CASCADE,
  UNIQUE(sample_id, row_index),
  UNIQUE(dataset_id, row_index)
);

-- 7) annotations
CREATE TABLE annotations (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  sample_id       INTEGER NOT NULL,
  row_index       INTEGER NOT NULL,
  evaluator_email VARCHAR(255) NOT NULL,
  label_id        INTEGER NOT NULL,
  created_at      DATETIME    DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(sample_id)       REFERENCES samples(id)       ON DELETE CASCADE,
  FOREIGN KEY(evaluator_email) REFERENCES evaluators(email) ON DELETE CASCADE,
  FOREIGN KEY(label_id)        REFERENCES dataset_labels(id) ON DELETE CASCADE,
  UNIQUE(sample_id, row_index, evaluator_email)
);
