"""Consultas e operações de eventos."""

from pathlib import Path

from db import conectar
from model import Evento


def listar_eventos(caminho_db: Path) -> list[Evento]:
    with conectar(caminho_db) as conexao:
        linhas = conexao.execute(
            "SELECT * FROM eventos ORDER BY data IS NULL, data ASC, horario ASC"
        ).fetchall()
    return [Evento.model_validate(dict(linha)) for linha in linhas]


def criar_evento(caminho_db: Path, evento: Evento) -> Evento:
    dados = evento.model_dump(exclude={"id"}, mode="json")
    with conectar(caminho_db) as conexao:
        cursor = conexao.execute(
            """INSERT INTO eventos (titulo, descricao, data, horario, local, link, situacao)
               VALUES (:titulo, :descricao, :data, :horario, :local, :link, :situacao)""",
            dados,
        )
    return evento.model_copy(update={"id": cursor.lastrowid})


def excluir_evento(caminho_db: Path, evento_id: int) -> bool:
    """Remove um evento existente e informa se havia conteúdo a excluir."""
    with conectar(caminho_db) as conexao:
        cursor = conexao.execute("DELETE FROM eventos WHERE id = ?", (evento_id,))
    return cursor.rowcount == 1
