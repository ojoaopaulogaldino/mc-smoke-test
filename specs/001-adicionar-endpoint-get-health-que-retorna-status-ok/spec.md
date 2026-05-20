# spec.md — 001-health-endpoint

> **Light Spec** — marcar uma.
> Esta spec é a fonte de verdade da feature. Código que diverge é bug, não criatividade.

## Objetivo

Expor um endpoint HTTP de verificação de saúde (`GET /health`) para permitir que orquestradores, load balancers e ferramentas de observabilidade confirmem que o serviço está em execução.

## Escopo

- Endpoint `GET /health` responde com status HTTP 200 e corpo JSON `{"status": "ok"}` quando o serviço está operacional.
- Teste automatizado pytest cobrindo o cenário de sucesso.

## Fora de escopo

- Verificação de dependências externas (banco de dados, filas, serviços downstream).
- Autenticação ou autorização no endpoint.
- Métricas detalhadas de saúde (uso de CPU, memória, versão do serviço).
- Endpoint `/ready` ou `/live` com semânticas distintas de liveness/readiness.
- [QUESTION: Deve o endpoint retornar informações adicionais como versão do serviço ou timestamp? O issue não menciona.]

## Requisitos funcionais

| ID | Requisito | Origem |
|----|-----------|--------|
| RF-001 | O endpoint `GET /health` deve retornar HTTP 200 | Issue #1 |
| RF-002 | O corpo da resposta deve ser exatamente `{"status": "ok"}` (JSON) | Issue #1 |
| RF-003 | O `Content-Type` da resposta deve ser `application/json` | Derivado de RF-002 (contrato JSON) |
| RF-004 | Deve existir ao menos um teste pytest cobrindo o endpoint | Issue #1 |

## Requisitos não-funcionais

| ID | Requisito | Limite mensurável |
|----|-----------|-------------------|
| RNF-001 | Latência p95 do endpoint | < 100ms (endpoint estático, sem I/O) |
| RNF-002 | Disponibilidade | Segue disponibilidade geral do serviço (99.9%) |

## Restrições e regulação aplicável

Criticidade lv1_light. Nenhuma regulação específica (LGPD, BACEN, OAB) se aplica a este endpoint — não há processamento de dados pessoais ou sensíveis.

[QUESTION: A constituição jsaai.md define alguma política de CORS ou rate limiting para endpoints públicos de health? Verificar `group-methodology/constitutions/jsaai.md`.]

## Contratos públicos afetados

| Contrato | Tipo | Mudança | Versão antes → depois |
|----------|------|---------|------------------------|
| `GET /health` | OpenAPI | criação | N/A → 1.0.0 |

## Casos de erro previstos

| Caso | Comportamento esperado | HTTP / código de erro |
|------|------------------------|-----------------------|
| Método HTTP não suportado (ex: POST /health) | [QUESTION: A framework deve retornar 405 Method Not Allowed automaticamente? Confirmar comportamento padrão do framework utilizado.] | 405 |

> Nota: Por ser um endpoint read-only sem input de usuário, os casos de erro são mínimos.

## Requisitos de segurança

Endpoint público, sem autenticação. Não recebe input de usuário e não acessa dados sensíveis. Não há privilege boundary a cruzar.

- Não deve expor stack traces, versões internas de dependências ou informações de infraestrutura na resposta.
- Nenhum threat model adicional requerido para criticidade lv1_light.

## Critérios de aceite

Ver `acceptance.md` (cenários BDD).

## Riscos identificados

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|------------|
| Endpoint expõe informações internas em futuras iterações | baixa | baixo | Manter resposta fixa no schema `{"status": "ok"}` conforme RF-002 |
| Framework roteador não registra a rota corretamente | baixa | baixo | Coberto pelo teste pytest (RF-004) |

---

**Criticidade:** **Light**
**HITL gate:** none
**Bounded context:** `modules/platform-observability/`
**Issue GitHub:** #1
**Mantenedor desta spec:** Product Analyst Agent (revisada por humano accountable)
