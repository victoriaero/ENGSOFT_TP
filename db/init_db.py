#!/usr/bin/env python3
import sqlite3
import pathlib

# Caminhos
BASE = pathlib.Path(__file__).parent
SCHEMA = BASE / "schema_sqlite.sql"
DBFILE = BASE / "datalabeler.db"

# Carrega o SQL
sql = SCHEMA.read_text()

# Cria/conecta e executa
conn = sqlite3.connect(DBFILE.as_posix())
# Habilita FK antes de rodar o script (a cláusula PRAGMA no SQL também seria suficiente,
# mas é bom garantir via API)
conn.execute("PRAGMA foreign_keys = ON;")
conn.executescript(sql)
conn.close()

print(f"Banco criado em {DBFILE}")
