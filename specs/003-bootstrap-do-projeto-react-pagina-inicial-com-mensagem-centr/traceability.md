# traceability.md — 003-react-bootstrap-home

> Matriz Requisito × Arquivo × Teste × Status.
> Atualizada pelo Implementation Agent (arquivos) e QA Agent (testes + status).
> Reviewer Agent verifica que está completa antes de aprovar PR.

## Matriz

| Requisito | Arquivo(s) implementador(es) | Teste(s) cobridor(es) | Status |
|-----------|------------------------------|------------------------|--------|
| RF-001 | `package.json`, `src/app/page.tsx` (ou `app/page.tsx`) | `tests/frontend-bootstrap/test_bootstrap.py::test_repository_has_minimum_structure` | red |
| RF-002 | `package.json` (script `dev`), `next.config.ts` | `tests/frontend-bootstrap/test_bootstrap.py::test_dev_server_starts_without_errors` | red |
| RF-003 | `package.json` (script `build`), `next.config.ts` | `tests/frontend-bootstrap/test_bootstrap.py::test_production_build_succeeds` | red |
| RF-004 | `src/app/page.tsx` (ou `app/page.tsx`) | `tests/frontend-bootstrap/test_bootstrap.py::test_home_displays_only_funcionou_text` | red |
| RF-005 | `src/app/globals.css` (ou `app/globals.css`) | `tests/frontend-bootstrap/test_bootstrap.py::test_funcionou_text_is_centered` | red |
| RF-006 | `package.json` (ausência de libs UI externas), `src/app/globals.css` | `tests/frontend-bootstrap/test_bootstrap.py::test_funcionou_text_is_centered` | red |
| RF-007 | `README.md` | `tests/frontend-bootstrap/test_bootstrap.py::test_readme_contains_execution_instructions` | red |
| RNF-001 | `next.config.ts`, ambiente Node 20 | `tests/frontend-bootstrap/test_bootstrap.py::test_dev_server_starts_without_errors` (timeout 30s) | red |
| RNF-002 | bundle gerado em `.next/static/` | `tests/frontend-bootstrap/test_bootstrap.py::test_production_build_succeeds` (presença de arquivos) | red |
| CA-001 | `package.json` (script `dev`), `src/app/page.tsx`, `next.config.ts` | `tests/frontend-bootstrap/test_bootstrap.py::test_dev_server_starts_without_errors` | red |
| CA-002 | `src/app/page.tsx` | `tests/frontend-bootstrap/test_bootstrap.py::test_home_displays_only_funcionou_text` | red |
| CA-003 | `src/app/globals.css` | `tests/frontend-bootstrap/test_bootstrap.py::test_funcionou_text_is_centered` | red |
| CA-004 | `package.json` (script `build`), `src/app/` | `tests/frontend-bootstrap/test_bootstrap.py::test_production_build_succeeds` | red |
| CA-005 | `package.json`, `src/app/`, `README.md`, `.gitignore` | `tests/frontend-bootstrap/test_bootstrap.py::test_repository_has_minimum_structure` | red |
| CA-006 | `README.md` | `tests/frontend-bootstrap/test_bootstrap.py::test_readme_contains_execution_instructions` | red |
| CA-007 | `package.json` (comportamento de erro sem deps) | `tests/frontend-bootstrap/test_bootstrap.py::test_dev_command_fails_without_node_modules` | red |

## Cobertura calculada

- **Requisitos funcionais cobertos:** 7/7 (100%)
- **Requisitos não-funcionais cobertos:** 2/2 (100%)
- **Critérios de aceite cobertos por teste passando:** 0/7 (0% — testes em estado RED; nenhum código de produção existe ainda)
- **Spec coverage gate (CAs):** lv1_light — gate será 100% após implementação

## ADRs vinculadas

| ADR | Aplicação nesta feature |
|-----|-------------------------|
| N/A — stack mandatória pela constituição JSAAI seção 2 | Next.js 15 + React 19 + pnpm já definidos; nenhuma ADR nova necessária para bootstrap trivial |

## Threat model vinculado (Critical only)

Não aplicável — feature lv1_light sem dados de usuário, sem autenticação, sem backend.

---

**Última atualização:** gerado por QA/Test Agent (CURRANTE — modo RED)  
**Reviewer Agent verificação:** pending
