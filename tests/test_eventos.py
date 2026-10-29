from datetime import date

import pytest
from pydantic import ValidationError

from model import Evento


def test_evento_aceita_dados_opcionais():
    evento = Evento(titulo="Encontro", descricao="Informações confirmadas", data=date(2026, 10, 29))
    assert evento.situacao == "proximo"


def test_evento_exige_titulo_valido():
    with pytest.raises(ValidationError):
        Evento(titulo="oi", descricao="Informações confirmadas")
