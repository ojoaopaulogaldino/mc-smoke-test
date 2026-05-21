# traceability.md — 003-react-bootstrap-home

> Matriz Requisito x Arquivo x Teste x Status.
> Atualizada pelo Implementation Agent (arquivos) e QA Agent (testes + status).
> Reviewer Agent verifica que esta completa antes de aprovar PR.

## Matriz

| Requisito | Arquivo(s) implementador(es) | Teste(s) cobridor(es) | Status |
|-----------|------------------------------|------------------------|--------|
| RF-001 | `package.json`, `src/app/page.tsx` (ou `app/page.tsx`) | `tests/frontend-bootstrap/test_bootstrap.py::test_repository_has_minimum_structure` | red |
| RF-002 | `package.json` (script `dev`) | `tests/frontend-bootstrap/test_bootstrap.py::test_dev_server_starts_without_errors` | red |
| RF-003 | `package.json` (script `build`) | `tests/frontend-bootstrap/test_bootstrap.py::test_production_build_succeeds` | red |
| RF-004 | `src/app/page.tsx` (ou `app/page.tsx`) | `tests/frontend-bootstrap/test_bootstrap.py::test_home_displays_only_funcionou_text` | red |
| RF-005 | `src/app/globals.css` (ou `app/globals.css`) | `tests/frontend-bootstrap/test_bootstrap.py::test_funcionou_text_is_centered` | red |
| RF-006 | `package.json` (ausencia de libs externas de UI) | `tests/frontend-bootstrap/test_bootstrap.py::test_home_displays_only_funcionou_text` | red |
| RF-007 | `README.md` | `tests/frontend-bootstrap/test_bootstrap.py::test_readme_contains_execution_instructions` | red |
| RNF-001 | `package.json` (script `dev`), servidor Next.js | `tests/frontend-bootstrap/test_bootstrap.py::test_dev_server_starts_without_errors` (timeout 30s) | red |
| RNF-002 | bundle gerado em `.next/` | inspecao manual do PR (QUESTION nao resolvida na spec) | pending |
| CA-001 | `package.json` + runtime Next.js 15 | `tests/frontend-bootstrap/test_bootstrap.py::test_dev_server_starts_without_errors` | red |
| CA-002 | `src/app/page.tsx` (ou `app/page.tsx`) | `tests/frontend-bootstrap/test_bootstrap.py::test_home_displays_only_funcionou_text` | red |
| CA-003 | `src/app/globals.css` (ou `app/globals.css`) | `tests/frontend-bootstrap/test_bootstrap.py::test_funcionou_text_is_centered` | red |
| CA-004 | `package.json` (script `build`) + Next.js build pipeline | `tests/frontend-bootstrap/test_bootstrap.py::test_production_build_succeeds` | red |
| CA-005 | `package.json`, `src/` ou `app/`, `README.md`, `.gitignore` | `tests/frontend-bootstrap/test_bootstrap.py::test_repository_has_minimum_structure` | red |
| CA-006 | `README.md` | `tests/frontend-bootstrap/test_bootstrap.py::test_readme_contains_execution_instructions` | red |
| CA-007 | comportamento de erro do runtime sem `node_modules/` | `tests/frontend-bootstrap/test_bootstrap.py::test_dev_command_fails_without_node_modules` | red |

## Cobertura calculada

- **Requisitos funcionais cobertos:** 7/7 (100%)
- **Requisitos nao-funcionais cobertos:** 1/2 (50%) — RNF-002 e QUESTION aberta na spec
- **Criterios de aceite cobertos por teste passando:** 0/7 (0%) — todos red (CURRANTE)
- **Spec coverage gate (CAs):** 0% atual (red); meta: 100% apos implementacao

## ADRs vinculadas

| ADR | Aplicacao nesta feature |
|-----|-------------------------|
| N/A — bootstrap trivial, sem ADR nova | Next.js 15 + React 19 + pnpm ja sao stack mandatoria pela constituicao JSAAI secao 2 |

## Threat model vinculado (Critical only)

N/A — feature lv1_light sem dados sensiveis, sem autenticacao, sem backend.

---

**Ultima atualizacao:** geracao CURRANTE por QA/Test Agent
**Reviewer Agent verificacao:** pending
