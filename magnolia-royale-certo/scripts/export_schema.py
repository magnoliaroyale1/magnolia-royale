"""Gera o esquema para estudo, sem ler registros nem credenciais do banco."""
from pathlib import Path
from sqlalchemy.schema import CreateTable, CreateIndex
from sqlalchemy.dialects.mysql import dialect
from backend.database import db
import backend.models

root = Path(__file__).resolve().parents[1]
destination = root / 'database'
destination.mkdir(exist_ok=True)
sql = ['-- Magnolia Royale: gerado a partir das Models. Use em uma base vazia.',
       'CREATE DATABASE IF NOT EXISTS magnolia_royale CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;',
       'USE magnolia_royale;']
for table in db.metadata.sorted_tables:
    sql.append(str(CreateTable(table).compile(dialect=dialect())).strip() + ';')
    for index in table.indexes:
        sql.append(str(CreateIndex(index).compile(dialect=dialect())) + ';')
(destination / 'schema.sql').write_text('\n\n'.join(sql)+'\n',encoding='utf-8')
print(f'Esquema gerado com {len(db.metadata.tables)} tabelas.')
