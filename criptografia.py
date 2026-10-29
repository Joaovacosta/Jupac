"""Hash de senha usando PBKDF2-HMAC da biblioteca padrão."""

import base64
import hashlib
import hmac
import os


def gerar_hash(senha: str) -> str:
    sal = os.urandom(16)
    derivada = hashlib.pbkdf2_hmac("sha256", senha.encode(), sal, 600_000)
    return f"pbkdf2_sha256$600000${base64.b64encode(sal).decode()}${base64.b64encode(derivada).decode()}"


def verificar_senha(senha: str, valor_hash: str) -> bool:
    try:
        algoritmo, iteracoes, sal, esperado = valor_hash.split("$", 3)
        if algoritmo != "pbkdf2_sha256":
            return False
        calculada = hashlib.pbkdf2_hmac(
            "sha256", senha.encode(), base64.b64decode(sal), int(iteracoes)
        )
        return hmac.compare_digest(calculada, base64.b64decode(esperado))
    except (ValueError, TypeError):
        return False
