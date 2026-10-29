"""Dependências de sessão para as rotas administrativas."""

from fastapi import HTTPException, Request, status


def exigir_admin(request: Request) -> None:
    if not request.session.get("admin"):
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/admin/login"})
