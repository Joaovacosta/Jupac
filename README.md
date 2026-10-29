# JUPAC

Site institucional de **Juventude Unida na Paz e no Amor de Cristo**. A primeira versão preserva a regra de não publicar informações sem confirmação: agenda, local, horários, imagens e demais dados ainda não fornecidos permanecem vazios ou editáveis no painel.

## Tecnologias

- Python, FastAPI e Jinja2;
- Pydantic para validação;
- SQLite local para eventos iniciais;
- HTML, CSS e JavaScript sem dependências de interface.

## Executar localmente

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app:app --reload
```

Abra `http://127.0.0.1:8000`. Para o painel, defina `ADMIN_USERNAME`, `ADMIN_PASSWORD_HASH` e um `SESSION_SECRET` seguro no `.env`. Gere o hash com `from criptografia import gerar_hash; print(gerar_hash("uma-senha-segura"))`.

## Testes

```powershell
pytest
```

## Estrutura

- `app.py`: rotas públicas e administrativas;
- `model.py`, `db.py` e `services/`: validação, persistência e regras de eventos;
- `templates/` e `static/`: páginas e interface;
- `tests/`: verificações de rotas e modelos.

## Publicação

Em produção, use uma variável `SESSION_SECRET` longa e exclusiva, HTTPS e um banco gerenciado antes de atender conteúdo de forma permanente. O arquivo `jupac.db` é local e está ignorado pelo Git.

As respostas públicas e administrativas incluem uma política de segurança de conteúdo (CSP), além de cabeçalhos contra incorporação e interpretação indevida de arquivos.
