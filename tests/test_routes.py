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


def test_respostas_incluem_cabecalhos_de_seguranca():
    with TestClient(app) as client:
        resposta = client.get("/")
        assert resposta.headers["x-content-type-options"] == "nosniff"
        assert resposta.headers["x-frame-options"] == "DENY"
        assert "default-src 'self'" in resposta.headers["content-security-policy"]


def test_404_tem_pagina_amigavel():
    with TestClient(app) as client:
        resposta = client.get("/nao-existe")
        assert resposta.status_code == 404
        assert "não foi encontrada" in resposta.text


def test_login_rejeita_formulario_sem_token_csrf():
    with TestClient(app) as client:
        resposta = client.post("/admin/login", data={"usuario": "admin", "senha": "senha-invalida"})
        assert resposta.status_code == 422


def test_pagina_de_login_mostra_token_csrf():
    with TestClient(app) as client:
        resposta = client.get("/admin/login")
        assert resposta.status_code == 200
        assert 'name="csrf_token"' in resposta.text
