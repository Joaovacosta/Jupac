"""Persistência SQLite simples para o conteúdo publicável do site."""

import sqlite3
from pathlib import Path


def conectar(caminho: Path) -> sqlite3.Connection:
    conexao = sqlite3.connect(caminho)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def inicializar(caminho: Path) -> None:
    with conectar(caminho) as conexao:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                data TEXT,
                horario TEXT,
                local TEXT,
                link TEXT,
                situacao TEXT NOT NULL DEFAULT 'proximo'
                    CHECK (situacao IN ('proximo', 'realizado', 'cancelado'))
            )
            """
        )
