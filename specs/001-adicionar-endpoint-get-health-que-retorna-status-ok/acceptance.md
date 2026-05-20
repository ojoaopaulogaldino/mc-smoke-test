# acceptance.md — 001-health-endpoint

> Cenários de aceite em formato BDD (Dado / Quando / Então).
> Cada cenário tem ID. QA/Test Agent deriva um teste por cenário (CURRANTE).
> Spec coverage gate calcula: (CAs cobertos por teste passando) / (CAs total).

## Cenários

### CA-001 — Retorno 200 com body correto

**Dado** que o serviço está em execução e acessível
**Quando** um cliente envia uma requisição `GET /health`
**Então** a resposta deve ter status HTTP 200
**E** o body da resposta deve ser exatamente `{"status": "ok"}`

### CA-002 — Content-Type JSON

**Dado** que o serviço está em execução e acessível
**Quando** um cliente envia uma requisição `GET /health`
**Então** o header `Content-Type` da resposta deve conter `application/json`

### CA-003 — Caso de erro: método HTTP não permitido

**Dado** que o serviço está em execução e acessível
**Quando** um cliente envia uma requisição `POST /health`
**Então** a resposta deve ter status HTTP 405

---

## Mapeamento CA → teste

Atualizado pelo QA/Test Agent ao escrever os testes (CURRANTE: red).
Atualizado pelo QA Agent ao validar (green + edge cases).

| CA | Arquivo de teste | Test function | Status |
|----|------------------|---------------|--------|
| CA-001 | `tests/platform_observability/test_health.py` | `test_health_returns_200_with_ok_body` | red |
| CA-002 | `tests/platform_observability/test_health.py` | `test_health_returns_json_content_type` | red |
| CA-003 | `tests/platform_observability/test_health.py` | `test_health_method_not_allowed` | red |

---

**Product Analyst Agent:** product-analyst-agent-v1
**Última revisão humana (se Lv.3):** N/A (HITL: none)
