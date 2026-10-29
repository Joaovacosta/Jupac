"""Aplicação institucional do JUPAC."""

import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware

from criptografia import verificar_senha
from db import inicializar
from model import Evento
from services.eventos_service import (
    atualizar_evento,
    buscar_evento,
    criar_evento,
    excluir_evento,
    listar_eventos,
)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "jupac.db"
load_dotenv(BASE_DIR / ".env")
INSTAGRAM_URL = "https://www.instagram.com/jupac.nsa/"


@asynccontextmanager
async def ciclo_vida(_: FastAPI):
    inicializar(DB_PATH)
    yield


app = FastAPI(title="JUPAC", description="Site institucional do JUPAC.", version="1.0.0", lifespan=ciclo_vida)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "troque-esta-chave-em-producao"), https_only=not __debug__, same_site="lax")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def pagina(request: Request, nome: str, **contexto: object) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name=nome, context={"instagram_url": INSTAGRAM_URL, **contexto})


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def pagina_inicial(request: Request) -> HTMLResponse:
    return pagina(request, "index.html", title="JUPAC — Juventude Unida na Paz e no Amor de Cristo", eventos=listar_eventos(DB_PATH)[:3])


@app.get("/quem-somos", response_class=HTMLResponse, include_in_schema=False)
def quem_somos(request: Request) -> HTMLResponse:
    return pagina(request, "sobre.html", title="Quem somos | JUPAC")


@app.get("/atividades", response_class=HTMLResponse, include_in_schema=False)
def atividades(request: Request) -> HTMLResponse:
    return pagina(request, "atividades.html", title="Atividades | JUPAC")


@app.get("/eventos", response_class=HTMLResponse, include_in_schema=False)
def eventos(request: Request) -> HTMLResponse:
    return pagina(request, "eventos.html", title="Agenda | JUPAC", eventos=listar_eventos(DB_PATH))


@app.get("/galeria", response_class=HTMLResponse, include_in_schema=False)
def galeria(request: Request) -> HTMLResponse:
    return pagina(request, "galeria.html", title="Galeria | JUPAC")


@app.get("/participar", response_class=HTMLResponse, include_in_schema=False)
def participar(request: Request) -> HTMLResponse:
    return pagina(request, "participar.html", title="Como participar | JUPAC")


@app.get("/admin/login", response_class=HTMLResponse, include_in_schema=False)
def login(request: Request) -> HTMLResponse:
    return pagina(request, "admin/login.html", title="Acesso administrativo | JUPAC")


@app.post("/admin/login", include_in_schema=False)
def efetuar_login(request: Request, usuario: str = Form(), senha: str = Form()) -> RedirectResponse:
    if usuario == os.getenv("ADMIN_USERNAME") and verificar_senha(senha, os.getenv("ADMIN_PASSWORD_HASH", "")):
        request.session["admin"] = True
        return RedirectResponse("/admin", status_code=status.HTTP_303_SEE_OTHER)
    return RedirectResponse("/admin/login?erro=1", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/admin", response_class=HTMLResponse, include_in_schema=False)
def painel(request: Request) -> HTMLResponse:
    if not request.session.get("admin"):
        return RedirectResponse("/admin/login", status_code=status.HTTP_303_SEE_OTHER)
    return pagina(request, "admin/dashboard.html", title="Painel | JUPAC", eventos=listar_eventos(DB_PATH))


@app.post("/admin/eventos", include_in_schema=False)
def cadastrar_evento(request: Request, titulo: str = Form(), descricao: str = Form(), data: str = Form(""), horario: str = Form(""), local: str = Form(""), link: str = Form(""), situacao: str = Form("proximo")) -> RedirectResponse:
    if not request.session.get("admin"):
        return RedirectResponse("/admin/login", status_code=status.HTTP_303_SEE_OTHER)
    evento = Evento.model_validate({"titulo": titulo, "descricao": descricao, "data": data or None, "horario": horario or None, "local": local or None, "link": link or None, "situacao": situacao})
    criar_evento(DB_PATH, evento)
    return RedirectResponse("/admin", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/admin/eventos/{evento_id}/editar", response_class=HTMLResponse, include_in_schema=False)
def formulario_edicao_evento(request: Request, evento_id: int):
    if not request.session.get("admin"):
        return RedirectResponse("/admin/login", status_code=status.HTTP_303_SEE_OTHER)
    evento = buscar_evento(DB_PATH, evento_id)
    if evento is None:
        return RedirectResponse("/admin", status_code=status.HTTP_303_SEE_OTHER)
    return pagina(request, "admin/evento_editar.html", title="Editar evento | JUPAC", evento=evento)


@app.post("/admin/eventos/{evento_id}/editar", include_in_schema=False)
def editar_evento(request: Request, evento_id: int, titulo: str = Form(), descricao: str = Form(), data: str = Form(""), horario: str = Form(""), local: str = Form(""), link: str = Form(""), situacao: str = Form("proximo")) -> RedirectResponse:
    if not request.session.get("admin"):
        return RedirectResponse("/admin/login", status_code=status.HTTP_303_SEE_OTHER)
    evento = Evento.model_validate({"titulo": titulo, "descricao": descricao, "data": data or None, "horario": horario or None, "local": local or None, "link": link or None, "situacao": situacao})
    atualizar_evento(DB_PATH, evento_id, evento)
    return RedirectResponse("/admin", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/admin/eventos/{evento_id}/excluir", include_in_schema=False)
def excluir_evento_publicado(request: Request, evento_id: int) -> RedirectResponse:
    if not request.session.get("admin"):
        return RedirectResponse("/admin/login", status_code=status.HTTP_303_SEE_OTHER)
    excluir_evento(DB_PATH, evento_id)
    return RedirectResponse("/admin", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/admin/sair", include_in_schema=False)
def sair(request: Request) -> RedirectResponse:
    request.session.clear()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/health", tags=["sistema"])
def verificar_saude() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/robots.txt", include_in_schema=False)
def robots() -> FileResponse:
    return FileResponse(BASE_DIR / "robots.txt", media_type="text/plain")


@app.get("/sitemap.xml", include_in_schema=False)
def sitemap() -> FileResponse:
    return FileResponse(BASE_DIR / "sitemap.xml", media_type="application/xml")


@app.exception_handler(StarletteHTTPException)
async def pagina_nao_encontrada(request: Request, exc: StarletteHTTPException) -> HTMLResponse:
    if exc.status_code == 404:
        resposta = pagina(request, "404.html", title="Página não encontrada | JUPAC")
        resposta.status_code = 404
        return resposta
    return HTMLResponse("Erro inesperado.", status_code=exc.status_code)
