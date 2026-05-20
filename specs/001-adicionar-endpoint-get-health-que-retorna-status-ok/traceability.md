# traceability.md — 001-health-endpoint

> Matriz Requisito × Arquivo × Teste × Status.
> Atualizada pelo Implementation Agent (arquivos) e QA Agent (testes + status).
> Reviewer Agent verifica que está completa antes de aprovar PR.

## Matriz

| Requisito | Arquivo(s) implementador(es) | Teste(s) cobridor(es) | Status |
|-----------|------------------------------|------------------------|--------|
| RF-001 | `modules/platform_observability/application/health_router.py` | `tests/platform-observability/test_health.py::test_health_returns_200_with_ok_body` | red |
| RF-002 | `modules/platform_observability/application/health_router.py` | `tests/platform-observability/test_health.py::test_health_returns_200_with_ok_body` | red |
| RF-003 | `modules/platform_observability/application/health_router.py` | `tests/platform-observability/test_health.py::test_health_returns_json_content_type` | red |
| RF-004 | `tests/platform-observability/test_health.py` | `tests/platform-observability/test_health.py::test_health_returns_200_with_ok_body`, `test_health_returns_json_content_type`, `test_health_post_returns_405` | red |
| RNF-001 | `modules/platform_observability/application/health_router.py` (sem I/O) | não coberto por teste automatizado nesta fase (lv1_light; monitoramento via middleware de métricas em produção) | pending |
| RNF-002 | infraestrutura (Cloud Run config) | smoke test em staging | pending |
| CA-001 | `modules/platform_observability/application/health_router.py`, `app/main.py` | `tests/platform-observability/test_health.py::test_health_returns_200_with_ok_body` | red |
| CA-002 | `modules/platform_observability/application/health_router.py`, `app/main.py` | `tests/platform-observability/test_health.py::test_health_returns_json_content_type` | red |
| CA-003 | `app/main.py` (roteamento FastAPI) | `tests/platform-observability/test_health.py::test_health_post_returns_405` | red |

## Cobertura calculada

- **Requisitos funcionais cobertos:** 4/4 (100%)
- **Requisitos não-funcionais cobertos:** 0/2 (0%) — RNF-001 e RNF-002 requerem infraestrutura de produção; fora do escopo de testes unitários/integração leve para lv1_light
- **Critérios de aceite cobertos por teste passando:** 0/3 (0%) — estado atual RED (CURRANTE); passará a 3/3 (100%) após implementação
- **Spec coverage gate (CAs):** meta 100% para lv1_light (3 CAs, 3 testes escritos, aguardando implementação para green)

## ADRs vinculadas

| ADR | Aplicação nesta feature |
|-----|-------------------------|
| N/A — sem ADR formal | Feature usa padrões já estabelecidos pela constituição jsaai.md: FastAPI (stack mandatória), pytest com uv, JSONResponse direto (sem Pydantic model) conforme mitigação de risco em plan.md |

## Threat model vinculado (Critical only)

Não aplicável — criticidade lv1_light, endpoint sem processamento de dados pessoais ou sensíveis.

---

**Última atualização:** geração CURRANTE (red) por qa-test-agent-v1
**Reviewer Agent verificação:** pending
