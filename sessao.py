"""Funções de sessão e proteção contra requisições forjadas."""

import secrets

from fastapi import HTTPException, Request, status


def exigir_admin(request: Request) -> None:
    if not request.session.get("admin"):
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/admin/login"})


def obter_token_csrf(request: Request) -> str:
    """Cria uma vez e mantém na sessão o token destinado aos formulários."""
    if "csrf_token" not in request.session:
        request.session["csrf_token"] = secrets.token_urlsafe(32)
    return request.session["csrf_token"]


def validar_token_csrf(request: Request, token: str) -> None:
    token_sessao = request.session.get("csrf_token", "")
    if not token_sessao or not secrets.compare_digest(token, token_sessao):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Formulário inválido ou expirado.")
