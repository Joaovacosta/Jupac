"""Modelos e validações da área de conteúdo do JUPAC."""

from datetime import date, time
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, Field, HttpUrl


class SituacaoEvento(StrEnum):
    PROXIMO = "proximo"
    REALIZADO = "realizado"
    CANCELADO = "cancelado"


class Evento(BaseModel):
    """Dados públicos de um evento, sem inventar informações obrigatórias."""

    id: int | None = None
    titulo: Annotated[str, Field(min_length=3, max_length=100)]
    descricao: Annotated[str, Field(min_length=3, max_length=800)]
    data: date | None = None
    horario: time | None = None
    local: Annotated[str, Field(max_length=160)] | None = None
    link: HttpUrl | None = None
    situacao: SituacaoEvento = SituacaoEvento.PROXIMO


class CredenciaisLogin(BaseModel):
    usuario: Annotated[str, Field(min_length=3, max_length=64)]
    senha: Annotated[str, Field(min_length=8, max_length=256)]
