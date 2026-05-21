# traceability.md — 001-health-endpoint

> Matriz Requisito × Arquivo × Teste × Status.
> Atualizada pelo Implementation Agent (arquivos) e QA Agent (testes + status).
> Reviewer Agent verifica que está completa antes de aprovar PR.

## Matriz

| Requisito | Arquivo(s) implementador(es) | Teste(s) cobridor(es) | Status |
|-----------|------------------------------|------------------------|--------|
| RF-001 | `modules/platform_observability/api/health.py` | `tests/platform_observability/test_health.py::test_health_returns_200_with_ok_body` | red |
| RF-002 | `modules/platform_observability/api/health.py` | `tests/platform_observability/test_health.py::test_health_returns_200_with_ok_body` | red |
| RF-003 | `modules/platform_observability/api/health.py` | `tests/platform_observability/test_health.py::test_health_returns_json_content_type` | red |
| RF-004 | `tests/platform_observability/test_health.py` | `tests/platform_observability/test_health.py::test_health_returns_200_with_ok_body`, `::test_health_returns_json_content_type`, `::test_health_method_not_allowed` | red |
| RNF-001 | `app/main.py` (Uvicorn config) | não coberto por teste de integração — monitoramento via middleware Prometheus (dívida técnica registrada em plan.md) | pending |
| RNF-002 | infraestrutura (Cloud Run / blue-green pipeline) | smoke test em staging — fora do escopo deste PR | pending |
| CA-001 | `modules/platform_observability/api/health.py`, `app/main.py` | `tests/platform_observability/test_health.py::test_health_returns_200_with_ok_body` | red |
| CA-002 | `modules/platform_observability/api/health.py`, `app/main.py` | `tests/platform_observability/test_health.py::test_health_returns_json_content_type` | red |
| CA-003 | `modules/platform_observability/api/health.py`, `app/main.py` | `tests/platform_observability/test_health.py::test_health_method_not_allowed` | red |

## Cobertura calculada

- **Requisitos funcionais cobertos:** 4/4 (100%)
- **Requisitos não-funcionais cobertos:** 0/2 (0%) — RNF-001 e RNF-002 requerem infraestrutura e não são cobertos por testes de integração neste PR
- **Critérios de aceite cobertos por teste passando:** 0/3 (0%) — modo CURRANTE (red); será 3/3 (100%) após implementação
- **Spec coverage gate (CAs):** Lv.1 light — gate ≥ 95%; atingível com 3/3 CAs verdes pós-implementação

## ADRs vinculadas

| ADR | Aplicação nesta feature |
|-----|-------------------------|
| N/A — sem ADR específica | Endpoint trivial de liveness usando FastAPI (stack mandatória pela constituição JSAAI §2). Sem trade-off arquitetural novo. |

## Threat model vinculado (Critical only)

Não aplicável — criticidade Lv.1 light; endpoint não trafega dados pessoais ou financeiros (spec.md §Restrições).

---

**Última atualização:** 2025-07-17T00:00:00Z por qa-test-agent-v1 (modo CURRANTE)
**Reviewer Agent verificação:** pending
