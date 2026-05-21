# traceability.md — 003-react-bootstrap-home

> Matriz Requisito × Arquivo × Teste × Status.
> Atualizada pelo Implementation Agent (arquivos) e QA Agent (testes + status).
> Reviewer Agent verifica que está completa antes de aprovar PR.

## Matriz

| Requisito | Arquivo(s) implementador(es) | Teste(s) cobridor(es) | Status |
|-----------|------------------------------|------------------------|--------|
| RF-001 | `package.json`, `src/app/page.tsx` (ou `app/page.tsx`), `src/` | `tests/frontend-bootstrap/test_bootstrap.py::test_repository_has_minimum_structure` | red |
| RF-002 | `package.json` (script `dev`), `next.config.ts` | `tests/frontend-bootstrap/test_bootstrap.py::test_dev_server_starts_without_errors` | red |
| RF-003 | `package.json` (script `build`), `next.config.ts` | `tests/frontend-bootstrap/test_bootstrap.py::test_production_build_succeeds` | red |
| RF-004 | `src/app/page.tsx` (ou `app/page.tsx`) | `tests/frontend-bootstrap/test_bootstrap.py::test_home_displays_only_funcionou_text` | red |
| RF-005 | `src/app/globals.css` (ou `app/globals.css`) | `tests/frontend-bootstrap/test_bootstrap.py::test_funcionou_text_is_centered` | red |
| RF-006 | `package.json` (ausência de libs de UI externas) | `tests/frontend-bootstrap/test_bootstrap.py::test_repository_has_minimum_structure` | red |
| RF-007 | `README.md` | `tests/frontend-bootstrap/test_bootstrap.py::test_readme_contains_execution_instructions` | red |
| RNF-001 | `next.config.ts`, hardware local | `tests/frontend-bootstrap/test_bootstrap.py::test_dev_server_starts_without_errors` (timeout=30s) | red |
| RNF-002 | `next.config.ts`, bundle gerado | `tests/frontend-bootstrap/test_bootstrap.py::test_production_build_succeeds` (bundle gerado em `.next/`) | red |
| CA-001 | `package.json` script `dev`, servidor Next.js | `tests/frontend-bootstrap/test_bootstrap.py::test_dev_server_starts_without_errors` | red |
| CA-002 | `src/app/page.tsx` (ou `app/page.tsx`) | `tests/frontend-bootstrap/test_bootstrap.py::test_home_displays_only_funcionou_text` | red |
| CA-003 | `src/app/globals.css` (ou `app/globals.css`), `src/app/page.tsx` | `tests/frontend-bootstrap/test_bootstrap.py::test_funcionou_text_is_centered` | red |
| CA-004 | `package.json` script `build`, `next.config.ts` | `tests/frontend-bootstrap/test_bootstrap.py::test_production_build_succeeds` | red |
| CA-005 | `package.json`, `src/` ou `app/`, `README.md`, `.gitignore` | `tests/frontend-bootstrap/test_bootstrap.py::test_repository_has_minimum_structure` | red |
| CA-006 | `README.md` | `tests/frontend-bootstrap/test_bootstrap.py::test_readme_contains_execution_instructions` | red |
| CA-007 | comportamento do runtime Node.js / pnpm sem node_modules | `tests/frontend-bootstrap/test_bootstrap.py::test_dev_command_fails_without_node_modules` | red |

## Cobertura calculada

- **Requisitos funcionais cobertos:** 7/7 (100%)
- **Requisitos não-funcionais cobertos:** 2/2 (100%)
- **Critérios de aceite cobertos por teste passando:** 0/7 (0%) — todos RED (CURRANTE: testes escritos antes da implementação)
- **Spec coverage gate (CAs):** 0% agora → meta 100% após implementação (lv1_light)

## ADRs vinculadas

| ADR | Aplicação nesta feature |
|-----|-------------------------|
| N/A — sem ADR formal | Next.js 15 + React 19 + pnpm são stack mandatória pela constituição JSAAI seção 2; nenhuma decisão arquitetural nova nesta feature |

## Threat model vinculado (Critical only)

N/A — feature lv1_light sem dados de usuário, sem autenticação, sem backend.

---

**Última atualização:** gerado pelo QA/Test Agent (CURRANTE) antes da implementação
**Reviewer Agent verificação:** pending
