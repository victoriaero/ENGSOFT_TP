import sqlite3

conn = sqlite3.connect("data_labeler.db")
cursor = conn.cursor()

# Tabela de usuários
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT CHECK(role IN ('dev', 'labeler')) NOT NULL
)
""")

# Tabela de datasets (criadas por desenvolvedores)
cursor.execute("""
CREATE TABLE IF NOT EXISTS datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    owner_id INTEGER NOT NULL,
    FOREIGN KEY(owner_id) REFERENCES users(id)
)
""")

# Tabela de controle de acesso (rotuladores que podem acessar cada dataset)
cursor.execute("""
CREATE TABLE IF NOT EXISTS dataset_access (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(dataset_id) REFERENCES datasets(id),
    FOREIGN KEY(user_id) REFERENCES users(id),
    UNIQUE(dataset_id, user_id)
)
""")

# Tabela de amostras (instâncias a serem rotuladas)
cursor.execute("""
CREATE TABLE IF NOT EXISTS samples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_id INTEGER NOT NULL,
    data TEXT NOT NULL,
    FOREIGN KEY(dataset_id) REFERENCES datasets(id)
)
""")

# Tabela de labels (por dataset)
cursor.execute("""
CREATE TABLE IF NOT EXISTS labels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY(dataset_id) REFERENCES datasets(id)
)
""")

# Tabela de anotações (registro da rotulação feita por um usuário para uma sample)
cursor.execute("""
CREATE TABLE IF NOT EXISTS annotations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(sample_id) REFERENCES samples(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# Tabela intermediária para armazenar múltiplas labels por anotação
cursor.execute("""
CREATE TABLE IF NOT EXISTS annotation_labels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    annotation_id INTEGER NOT NULL,
    label_id INTEGER NOT NULL,
    FOREIGN KEY(annotation_id) REFERENCES annotations(id),
    FOREIGN KEY(label_id) REFERENCES labels(id),
    UNIQUE(annotation_id, label_id)
)
""")

conn.commit()
conn.close()

print("Banco de dados 'data_labeler.db' criado com sucesso.")
