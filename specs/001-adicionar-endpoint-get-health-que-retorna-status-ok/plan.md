# plan.md — 001-health-endpoint

> Plano técnico. Como vamos implementar a `spec.md`.
> Architect Agent escreve. Implementation Agent consome.

## Sequência técnica

1. Criar estrutura do módulo `modules/platform-observability/` (com `__init__.py` no pacote e subdiretórios `application/` para o router FastAPI).
2. Implementar o router FastAPI com endpoint `GET /health` retornando `JSONResponse({"status": "ok"})` com status 200 em `modules/platform-observability/application/health_router.py`.
3. Registrar o router na aplicação FastAPI principal (ou criar `app/main.py` mínimo se ainda não existir) via `app.include_router(health_router)`.
4. Criar diretório `tests/platform-observability/` com `__init__.py` e implementar os 3 testes pytest (CA-001, CA-002, CA-003) usando `fastapi.testclient.TestClient`.
5. Rodar `uv run pytest tests/platform-observability/ -v` localmente para confirmar verde.

## Arquivos prováveis

| Arquivo | Mudança esperada |
|---------|-------------------|
| `modules/platform-observability/__init__.py` | criar (vazio) |
| `modules/platform-observability/application/__init__.py` | criar (vazio) |
| `modules/platform-observability/application/health_router.py` | criar — define `APIRouter` com `GET /health` |
| `app/main.py` | criar ou modificar — instanciar `FastAPI()` e `include_router(health_router)` |
| `tests/platform-observability/__init__.py` | criar (vazio) |
| `tests/platform-observability/test_health.py` | criar — testes `test_health_returns_200_with_ok_body`, `test_health_returns_json_content_type`, `test_health_post_returns_405` |
| `pyproject.toml` | modificar se necessário — garantir `fastapi`, `httpx` (TestClient) e `pytest` como deps |

## ADRs vinculadas

**Sem ADR — uso de padrões já estabelecidos.**

Feature não introduz contrato público novo de negócio (health endpoint é padrão operacional universal), não cria invariante arquitetural novo, não abre trade-off não-óbvio (FastAPI já é stack mandatória pela constituição), não adiciona dependência externa e não muda política de segurança.

## Plano de testes (alto nível)

- **Unit / Integration leve:** 3 testes em `tests/platform-observability/test_health.py` usando `TestClient` do FastAPI. Cobrem CA-001 (200 + body), CA-002 (Content-Type) e CA-003 (405 em POST).
- **E2E:** não aplicável para Lv.1; o teste com TestClient já exercita o roteamento real do FastAPI.
- **Contract:** o contrato `GET /health → 200 {"status":"ok"}` é verificado diretamente pelos testes CA-001 e CA-002. OpenAPI schema é gerado automaticamente pelo FastAPI; não há schema externo a versionar nesta primeira versão.

## Plano de observabilidade

| Sinal | Tipo | Onde | Threshold |
|-------|------|------|-----------|
| `http_requests_total{route="/health"}` | counter | middleware FastAPI / endpoint | n/a (apenas contagem) |
| `http_request_duration_seconds{route="/health"}` | histogram | middleware FastAPI | alerta p95 > 100ms por 5min (RNF-001) |
| `http_requests_errors_total{route="/health",status=~"5.."}` | counter | middleware FastAPI | alerta > 1/min (endpoint estático não deve falhar) |

> Nota: como o endpoint é estático e sem I/O, espera-se latência p95 << 100ms. Se o serviço já possui middleware genérico de métricas HTTP, o endpoint herda automaticamente — não criar instrumentação dedicada.

## Plano de rollback

Criticidade Lv.1 → rollback padrão pelo pipeline blue-green.

- Como reverter código: `git revert <SHA do merge>` + redeploy via pipeline padrão.
- Como reverter dados: N/A — feature não toca persistência.
- Janela de detecção: deploy padrão; endpoint começa a ser consumido por LB/orquestrador imediatamente. Se health passar a falhar em produção, o próprio LB sinaliza.
- Sinais que disparam rollback: taxa de 5xx em `/health` > 1% por 5min, ou p95 > 500ms sustentado por 10min.

## Riscos técnicos

| Risco | Mitigação |
|-------|-----------|
| Router não é registrado na app principal (rota 404) | Teste CA-001 via TestClient pega isso antes do merge |
| Resposta padrão do FastAPI inclui campos extras além de `{"status":"ok"}` (ex: usar Pydantic model com campos opcionais default) | Usar `JSONResponse` direto com dict literal, não modelo Pydantic, garantindo igualdade exata do body |
| Middleware global de auth/CORS bloqueia `/health` involuntariamente | Documentar `/health` como rota pública isenta de auth na configuração de middleware, e validar via TestClient sem credenciais |
| Conflito de rota se outro módulo já expõe `/health` | Grep no repo antes de criar; se existir, consolidar ao invés de duplicar |

---

**Architect Agent:** architect-agent-v1
**Reviewed by:** N/A (Lv.1, HITL: none)
**Próximo passo:** EM decompõe em `tasks.md`.
