# traceability.md — 003-react-bootstrap-home

> Matriz Requisito × Arquivo × Teste × Status.
> Atualizada pelo Implementation Agent (arquivos) e QA Agent (testes + status).
> Reviewer Agent verifica que está completa antes de aprovar PR.

## Matriz

| Requisito | Arquivo(s) implementador(es) | Teste(s) cobridor(es) | Status |
|-----------|------------------------------|------------------------|--------|
| RF-001 | `src/app/page.tsx`, `package.json`, `src/` | `tests/frontend-bootstrap/test_bootstrap.py::test_repository_has_minimum_structure` | red |
| RF-002 | `package.json` (script `dev`) | `tests/frontend-bootstrap/test_bootstrap.py::test_dev_server_starts_without_errors` | red |
| RF-003 | `package.json` (script `build`) | `tests/frontend-bootstrap/test_bootstrap.py::test_production_build_succeeds` | red |
| RF-004 | `src/app/page.tsx` | `tests/frontend-bootstrap/test_bootstrap.py::test_home_displays_only_funcionou_text` | red |
| RF-005 | `src/app/globals.css` | `tests/frontend-bootstrap/test_bootstrap.py::test_funcionou_text_is_centered` | red |
| RF-006 | `package.json` (ausência de libs de UI), `src/app/globals.css` | `tests/frontend-bootstrap/test_bootstrap.py::test_home_displays_only_funcionou_text` | red |
| RF-007 | `README.md` | `tests/frontend-bootstrap/test_bootstrap.py::test_readme_contains_execution_instructions` | red |
| RNF-001 | `package.json` (script `dev`), Next.js runtime | `tests/frontend-bootstrap/test_bootstrap.py::test_dev_server_starts_without_errors` (timeout 30s) | red |
| RNF-002 | `.next/` (bundle gerado) | `tests/frontend-bootstrap/test_bootstrap.py::test_production_build_succeeds` (verifica artefatos) | red |
| CA-001 | `package.json`, Next.js dev server | `tests/frontend-bootstrap/test_bootstrap.py::test_dev_server_starts_without_errors` | red |
| CA-002 | `src/app/page.tsx` | `tests/frontend-bootstrap/test_bootstrap.py::test_home_displays_only_funcionou_text` | red |
| CA-003 | `src/app/globals.css` | `tests/frontend-bootstrap/test_bootstrap.py::test_funcionou_text_is_centered` | red |
| CA-004 | `package.json`, Next.js build | `tests/frontend-bootstrap/test_bootstrap.py::test_production_build_succeeds` | red |
| CA-005 | `package.json`, `src/`, `README.md`, `.gitignore` | `tests/frontend-bootstrap/test_bootstrap.py::test_repository_has_minimum_structure` | red |
| CA-006 | `README.md` | `tests/frontend-bootstrap/test_bootstrap.py::test_readme_contains_execution_instructions` | red |
| CA-007 | `package.json` (comportamento sem node_modules) | `tests/frontend-bootstrap/test_bootstrap.py::test_dev_command_fails_without_node_modules` | red |

## Cobertura calculada

- **Requisitos funcionais cobertos:** 7/7 (100%)
- **Requisitos não-funcionais cobertos:** 2/2 (100%)
- **Critérios de aceite cobertos por teste passando:** 0/7 (0%) — todos RED (CURRANTE: testes escritos antes do código)
- **Spec coverage gate (CAs):** lv1_light — alvo ≥ 95% ao final; atualmente 0% pois implementação não existe

## ADRs vinculadas

| ADR | Aplicação nesta feature |
|-----|-------------------------|
| N/A (stack mandatória) | Next.js 15 + React 19 + TypeScript já definidos na constituição JSAAI seção 2; nenhum ADR novo necessário para bootstrap trivial |

## Threat model vinculado (Critical only)

N/A — feature lv1_light sem dados de usuário, sem autenticação, sem backend.

---

**Última atualização:** gerado pelo QA/Test Agent (CURRANTE) — testes RED antes da implementação
**Reviewer Agent verificação:** pending
