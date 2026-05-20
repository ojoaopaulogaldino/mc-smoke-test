# tasks.md — 001-health-endpoint

> Decomposição executável. Engineering Manager decompõe `plan.md` em tasks que cabem em uma sessão de Implementation Agent.

## Tasks

### T-001 — Garantir dependências no pyproject.toml

- **Objetivo:** Assegurar que `fastapi`, `httpx` (necessário para TestClient) e `pytest` estão declarados como dependências do projeto.
- **Input:** `pyproject.toml` atual.
- **Output:** `pyproject.toml` atualizado com as três dependências; `uv sync` executa sem erros.
- **Critério de validação:** `uv run python -c "import fastapi, httpx, pytest"` sai com código 0.
- **Estimativa:** S
- **Bloqueadores:** nenhum

### T-002 — Criar estrutura de pacotes do módulo platform-observability

- **Objetivo:** Criar diretórios e `__init__.py` vazios para `modules/platform-observability/` e `modules/platform-observability/application/`.
- **Input:** repositório limpo.
- **Output:** dois `__init__.py` vazios criados nos caminhos corretos.
- **Critério de validação:** `uv run python -c "import importlib; importlib.import_module('modules.platform-observability.application')"` (ou equivalente via pathlib) confirma que os diretórios e arquivos existem.
- **Estimativa:** S
- **Bloqueadores:** T-001

### T-003 — Criar testes pytest derivados de acceptance.md (CURRANTE: red)

- **Objetivo:** Escrever os 3 testes (CA-001, CA-002, CA-003) em `tests/platform-observability/test_health.py` usando `TestClient`, antes da implementação. Criar também `tests/platform-observability/__init__.py` vazio.
- **Input:** `acceptance.md` (cenários CA-001 a CA-003).
- **Output:** Arquivo de testes contendo `test_health_returns_200_with_ok_body`, `test_health_returns_json_content_type`, `test_health_post_returns_405`.
- **Critério de validação:** `uv run pytest tests/platform-observability/ -v` executa os 3 testes e todos falham (red) por ausência do endpoint — confirma que os testes estão ativos e detectam ausência da feature.
- **Estimativa:** M
- **Bloqueadores:** T-002

### T-004 — Implementar health_router com endpoint GET /health

- **Objetivo:** Criar `modules/platform-observability/application/health_router.py` com `APIRouter` expondo `GET /health` que retorna `JSONResponse({"status": "ok"})` com status 200. Usar `JSONResponse` direto (não Pydantic model) para garantir body exato.
- **Input:** spec do contrato e mitigação de risco do plan.md.
- **Output:** módulo `health_router.py` com `router = APIRouter()` exportado.
- **Critério de validação:** `uv run python -c "from modules.platform_observability.application.health_router import router; print(router.routes)"` lista a rota `/health` com método GET.
- **Estimativa:** S
- **Bloqueadores:** T-003

### T-005 — Registrar health_router em app/main.py

- **Objetivo:** Criar (ou modificar) `app/main.py` para instanciar `FastAPI()` e chamar `app.include_router(health_router)`. Garantir que `/health` permaneça isento de eventuais middlewares de auth.
- **Input:** `health_router` de T-004.
- **Output:** `app/main.py` exportando `app` com rota `/health` registrada.
- **Critério de validação:** `uv run pytest tests/platform-observability/ -v` passa nos 3 testes (CA-001, CA-002, CA-003) — green.
- **Estimativa:** S
- **Bloqueadores:** T-004

### T-006 — Validação final e suíte completa verde

- **Objetivo:** Rodar a suíte completa de testes do repositório para garantir que nenhuma regressão foi introduzida e que o módulo está integrado.
- **Input:** código completo após T-005.
- **Output:** evidência de execução verde.
- **Critério de validação:** `uv run pytest -v` sai com código 0 e os 3 testes de health aparecem como `PASSED`.
- **Estimativa:** S
- **Bloqueadores:** T-005

---

## Progress ledger (espelho leve do Convex)

| ID | Status | Owner | Iniciada | Concluída |
|----|--------|-------|----------|-----------|
| T-001 | pending | — | — | — |
| T-002 | pending | — | — | — |
| T-003 | pending | — | — | — |
| T-004 | pending | — | — | — |
| T-005 | pending | — | — | — |
| T-006 | pending | — | — | — |

> O progress ledger autoritativo está em `progress_ledger` no Convex. Esta tabela é espelho legível por humano.

---

**EM Agent:** engineering-manager-agent-v1
**Próximo passo:** QA/Test Agent valida que T-003 está corretamente em red antes de Implementation Agent iniciar T-004.
