"""Ponto de entrada da aplicação institucional do JUPAC."""

from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = FastAPI(
    title="JUPAC — Juventude Unida na Paz e no Amor de Cristo",
    description="Site institucional do grupo de jovens JUPAC.",
    version="0.1.0",
)


@app.get("/health", tags=["sistema"])
def verificar_saude() -> dict[str, str]:
    """Informa que a aplicação está disponível."""
    return {"status": "ok"}
