# spec.md — 001-health-endpoint

> **Light Spec** — marcar uma.
> Esta spec é a fonte de verdade da feature. Código que diverge é bug, não criatividade.

## Objetivo

Expor um endpoint HTTP `GET /health` para que ferramentas de monitoramento e smoke tests possam verificar rapidamente se o serviço está no ar, sem necessidade de autenticação.

## Escopo

- Endpoint `GET /health` responde com body JSON `{"status": "ok"}` e HTTP 200.
- Teste automatizado com pytest que valida o comportamento do endpoint.

## Fora de escopo

- Verificação de dependências internas (banco de dados, filas, serviços externos) — apenas liveness superficial.
- Autenticação ou autorização no endpoint.
- Métricas detalhadas de saúde (readiness, startup probes diferenciados).
- Versionamento do endpoint (ex.: `/v1/health`).

## Requisitos funcionais

| ID | Requisito | Origem |
|----|-----------|--------|
| RF-001 | O endpoint `GET /health` deve retornar HTTP 200 | Issue #1 |
| RF-002 | O corpo da resposta deve ser exatamente `{"status": "ok"}` (JSON) | Issue #1 |
| RF-003 | O header `Content-Type` da resposta deve ser `application/json` | Derivado de RF-002 (contrato JSON) |
| RF-004 | Deve existir ao menos um teste pytest cobrindo o endpoint | Issue #1 |

## Requisitos não-funcionais

| ID | Requisito | Limite mensurável |
|----|-----------|-------------------|
| RNF-001 | Latência p95 do endpoint | < 200ms |
| RNF-002 | Disponibilidade | 99.9% |

## Restrições e regulação aplicável

- **Criticidade lv1_light**: nenhuma regulação específica (LGPD, BACEN, OAB) se aplica a este endpoint, pois não trafega dados pessoais ou financeiros.
- O endpoint deve ser acessível sem autenticação para permitir checks externos de infraestrutura (load balancers, orquestradores).

[QUESTION: Há alguma restrição de rede (ex.: endpoint só acessível internamente) ou o health check deve ser público?]

## Contratos públicos afetados

| Contrato | Tipo | Mudança | Versão antes → depois |
|----------|------|---------|------------------------|
| `GET /health` | OpenAPI | criação | N/A → 1.0.0 |

[QUESTION: Existe um arquivo OpenAPI/Swagger já versionado para este serviço? Se sim, qual a versão atual?]

## Casos de erro previstos

| Caso | Comportamento esperado | HTTP / código de erro |
|------|------------------------|-----------------------|
| Método não permitido (ex.: POST /health) | Retorna erro de método não permitido | 405 |

> Para este endpoint simples de liveness, não há casos de erro de negócio previstos além de método inválido.

## Requisitos de segurança

- **Threat model (Light):** O endpoint não recebe input do cliente (sem query params, sem body), portanto a superfície de ataque é mínima.
- Nenhum dado sensível é exposto na resposta.
- Não há privilege boundary a proteger.
- Recomendação: garantir que o endpoint não exponha informações de versão interna do framework ou stack trace em nenhuma circunstância.

## Critérios de aceite

Ver `acceptance.md` (cenários BDD).

## Riscos identificados

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|------------|
| Endpoint expor informações sensíveis do servidor em headers de resposta | baixa | baixo | Revisar headers padrão do framework (ex.: `Server`, `X-Powered-By`) e remover se necessário |
| Teste pytest não executado no CI | baixa | baixo | Garantir que pytest está no pipeline de CI e o teste está no diretório correto |

---

**Criticidade:** **Light**
**HITL gate:** none
**Bounded context:** `modules/platform-observability/`
**Issue GitHub:** #1
**Mantenedor desta spec:** Product Analyst Agent (revisada por humano accountable)
