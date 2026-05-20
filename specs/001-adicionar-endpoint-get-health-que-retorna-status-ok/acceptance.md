# acceptance.md — 001-health-endpoint

> Cenários de aceite em formato BDD (Dado / Quando / Então).
> Cada cenário tem ID. QA/Test Agent deriva um teste por cenário (CURRANTE).
> Spec coverage gate calcula: (CAs cobertos por teste passando) / (CAs total).

## Cenários

### CA-001 — Retorno de status 200 com corpo JSON correto

**Dado** que o serviço está em execução
**Quando** uma requisição `GET /health` é enviada sem body e sem headers especiais
**Então** a resposta HTTP deve ter status code `200`
**E** o corpo da resposta deve ser exatamente `{"status": "ok"}`

### CA-002 — Content-Type da resposta é application/json

**Dado** que o serviço está em execução
**Quando** uma requisição `GET /health` é enviada
**Então** o header `Content-Type` da resposta deve conter `application/json`

### CA-003 — Caso de erro: método HTTP não suportado

**Dado** que o serviço está em execução
**Quando** uma requisição `POST /health` é enviada (método não suportado)
**Então** a resposta HTTP deve ter status code `405` (Method Not Allowed)
**E** o corpo não deve conter stack traces ou informações internas de infraestrutura

---

## Mapeamento CA → teste

Atualizado pelo QA/Test Agent ao escrever os testes (CURRANTE: red).
Atualizado pelo QA Agent ao validar (green + edge cases).

| CA | Arquivo de teste | Test function | Status |
|----|------------------|---------------|--------|
| CA-001 | `tests/platform-observability/test_health.py` | `test_health_returns_200_with_ok_body` | red |
| CA-002 | `tests/platform-observability/test_health.py` | `test_health_returns_json_content_type` | red |
| CA-003 | `tests/platform-observability/test_health.py` | `test_health_post_returns_405` | red |

---

**Product Analyst Agent:** product-analyst-agent-v1
**Última revisão humana (se Lv.3):** N/A (HITL: none)
