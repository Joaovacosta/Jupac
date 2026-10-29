from fastapi.testclient import TestClient

from app import app


def test_paginas_publicas_disponiveis():
    with TestClient(app) as client:
        for rota in ("/", "/quem-somos", "/atividades", "/eventos", "/galeria", "/participar"):
            resposta = client.get(rota)
            assert resposta.status_code == 200


def test_health_disponivel():
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}


def test_404_tem_pagina_amigavel():
    with TestClient(app) as client:
        resposta = client.get("/nao-existe")
        assert resposta.status_code == 200
        assert "não foi encontrada" in resposta.text
