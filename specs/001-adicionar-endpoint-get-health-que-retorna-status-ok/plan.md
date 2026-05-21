# plan.md — 001-health-endpoint

> Plano técnico. Como vamos implementar a `spec.md`.
> Architect Agent escreve. Implementation Agent consome.

## Sequência técnica

1. Criar estrutura inicial do bounded context `platform-observability` (se ainda não existir): `modules/platform_observability/__init__.py` e subdiretórios `api/`, `application/`.
2. Implementar router FastAPI com endpoint `GET /health` em `modules/platform_observability/api/health.py` retornando `{"status": "ok"}` com HTTP 200 e `Content-Type: application/json` (default do FastAPI via `JSONResponse`).
3. Registrar o router no app FastAPI principal (`main.py` ou `app/main.py` conforme estrutura existente). Se app ainda não existe, criar `app/main.py` mínimo com `FastAPI()` e `include_router`.
4. Garantir que o método `POST /health` retorne 405 automaticamente (comportamento default do FastAPI quando rota só aceita GET — validar com teste).
5. Criar diretório de testes `tests/platform_observability/` com `__init__.py` e implementar `tests/platform_observability/test_health.py` cobrindo CA-001, CA-002, CA-003 usando `TestClient` do FastAPI.
6. Validar headers de resposta: remover/ocultar headers de exposição de stack (ex.: `server`) via middleware mínimo ou configuração de Uvicorn — apenas se default expuser informação sensível; caso contrário, deixar nota.
7. Rodar `pytest` localmente e garantir 3 testes verdes.

## Arquivos prováveis

| Arquivo | Mudança esperada |
|---------|-------------------|
| `modules/platform_observability/__init__.py` | criar (vazio) |
| `modules/platform_observability/api/__init__.py` | criar (vazio) |
| `modules/platform_observability/api/health.py` | criar (router com `GET /health`) |
| `app/main.py` | criar ou modificar (registrar router) |
| `tests/platform_observability/__init__.py` | criar (vazio) |
| `tests/platform_observability/test_health.py` | criar (3 testes: CA-001, CA-002, CA-003) |

## ADRs vinculadas

**Sem ADR — uso de padrões já estabelecidos.** Endpoint trivial de liveness usando FastAPI (stack mandatória pela constituição). Sem trade-off arquitetural, sem nova dependência, sem mudança de contrato relevante além da criação trivial.

## Plano de testes (alto nível)

- Unit: nenhum (endpoint não tem lógica de domínio).
- Integration: 3 testes usando `fastapi.testclient.TestClient` cobrindo os 3 CAs de `acceptance.md`.
- E2E: não aplicável para esta feature (smoke test externo virá via infra de monitoramento).
- Contract: validação do shape `{"status": "ok"}` já coberta no teste de integração; se houver OpenAPI versionado no repo, atualizar; caso contrário, FastAPI gera automaticamente em `/openapi.json`.

## Plano de observabilidade

| Sinal | Tipo | Onde | Threshold |
|-------|------|------|-----------|
| `health_request_total` | counter | endpoint `GET /health` | n/a (informativo) |
| `health_latency_seconds` | histogram | endpoint `GET /health` | alerta p95 > 200ms por 5min (alinhado com RNF-001) |
| `health_5xx_total` | counter | endpoint `GET /health` | alerta > 1/min (qualquer 5xx em liveness é anômalo) |

Obs.: instrumentação via middleware Prometheus padrão do app (se já existir). Se ainda não houver, registrar como dívida — não bloqueia entrega Lv.1.

## Plano de rollback

Criticidade Lv.1 → **rollback padrão pelo pipeline blue-green**.

- Como reverter código: `git revert <SHA>` + redeploy via pipeline padrão.
- Como reverter dados: não aplicável (sem persistência).
- Janela de detecção: canário padrão de 10min antes de full rollout.
- Sinais que disparam rollback: `health_5xx_total > 1/min` no canário ou falha no smoke test do pipeline.

## Riscos técnicos

| Risco | Mitigação |
|-------|-----------|
| Headers default do FastAPI/Uvicorn exporem versão (`server: uvicorn`) | Inspecionar resposta no teste; se necessário, configurar `server_header=False` no Uvicorn |
| Rota `/health` colidir com prefixo já existente | Verificar `app/main.py` antes de registrar; se houver conflito, alinhar com EM |
| Teste não rodar no CI por falta de descoberta (path) | Garantir `pytest.ini`/`pyproject.toml` inclui `tests/` no `testpaths` |

---

**Architect Agent:** architect-agent-v1
**Reviewed by:** N/A (Lv.1, HITL: none)
**Próximo passo:** EM decompõe em `tasks.md`.
