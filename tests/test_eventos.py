from datetime import date

import pytest
from pydantic import ValidationError

from model import Evento
from services.eventos_service import criar_evento, excluir_evento, listar_eventos


def test_evento_aceita_dados_opcionais():
    evento = Evento(titulo="Encontro", descricao="Informações confirmadas", data=date(2026, 10, 29))
    assert evento.situacao == "proximo"


def test_evento_exige_titulo_valido():
    with pytest.raises(ValidationError):
        Evento(titulo="oi", descricao="Informações confirmadas")


def test_exclusao_remove_somente_evento_existente(tmp_path):
    caminho_db = tmp_path / "eventos.db"
    from db import inicializar

    inicializar(caminho_db)
    criado = criar_evento(caminho_db, Evento(titulo="Encontro", descricao="Informações confirmadas"))

    assert excluir_evento(caminho_db, criado.id or 0) is True
    assert listar_eventos(caminho_db) == []
    assert excluir_evento(caminho_db, criado.id or 0) is False
