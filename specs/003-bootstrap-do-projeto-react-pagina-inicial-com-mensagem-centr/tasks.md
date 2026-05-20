# tasks.md — 003-react-bootstrap-home

> Decomposição executável. Engineering Manager decompõe `plan.md` em tasks que cabem em uma sessão de Implementation Agent.

## Tasks

### T-001 — Bootstrap projeto Next.js 15 + React 19

- **Objetivo:** Inicializar projeto Next.js 15 com React 19 e TypeScript na raiz do repositório, sem libs externas de UI.
- **Input:** Repositório vazio, pnpm e Node 20 instalados.
- **Output:** `package.json`, `pnpm-lock.yaml`, `tsconfig.json`, `next.config.ts`, `.gitignore`, pasta `app/` e `public/` gerados via `pnpm create next-app@latest . --typescript --app --no-tailwind --no-eslint --no-src-dir --import-alias '@/*'`. Apenas `next`, `react`, `react-dom` em `dependencies`; `@types/*` em `devDependencies`.
- **Critério de validação:** `tests/frontend-bootstrap/test_repository_structure.py::test_repo_has_minimum_structure` e `test_no_external_ui_library_dependency` passam.
- **Estimativa:** S
- **Bloqueadores:** nenhum

### T-002 — Pin de versão do Node 20 LTS

- **Objetivo:** Fixar versão do Node.js para garantir reprodutibilidade.
- **Input:** `package.json` da T-001.
- **Output:** `.nvmrc` na raiz com conteúdo `20`; campo `engines.node` em `package.json` apontando para `>=20 <21`.
- **Critério de validação:** arquivo `.nvmrc` existe e contém `20`; `package.json` tem `engines.node`. Verificado em `tests/frontend-bootstrap/test_repository_structure.py::test_repo_has_minimum_structure`.
- **Estimativa:** S
- **Bloqueadores:** T-001

### T-003 — Limpar boilerplate do Next.js

- **Objetivo:** Remover conteúdo demo gerado pelo `create-next-app`.
- **Input:** `app/page.tsx`, `app/globals.css`, `app/layout.tsx` com conteúdo demo.
- **Output:** `app/page.tsx` esvaziado (placeholder mínimo), `app/globals.css` sem estilos demo, `app/layout.tsx` sem fontes/decoração demo. Favicon default pode ficar.
- **Critério de validação:** `pnpm build` finaliza com exit 0 sem warnings críticos. Nenhum texto demo (`Get started`, `Vercel`, etc.) presente em `app/`.
- **Estimativa:** S
- **Bloqueadores:** T-001

### T-004 — Root layout mínimo em pt-BR

- **Objetivo:** Configurar `app/layout.tsx` com `<html lang="pt-BR">` e metadata mínima.
- **Input:** `app/layout.tsx` limpo da T-003.
- **Output:** `app/layout.tsx` com `<html lang="pt-BR">`, `metadata = { title: 'JSAAI', description: '...' }`, sem imports de fontes externas, importando `./globals.css`.
- **Critério de validação:** `pnpm build` passa; HTML renderizado contém `lang="pt-BR"` e `<title>JSAAI</title>`.
- **Estimativa:** S
- **Bloqueadores:** T-003

### T-005 — Implementar home renderizando "funcionou"

- **Objetivo:** `app/page.tsx` como Server Component renderiza apenas a string `funcionou` dentro de `<main>`.
- **Input:** `app/page.tsx` placeholder da T-003.
- **Output:** `app/page.tsx` exporta default Server Component que retorna `<main>funcionou</main>` (com classe ou estrutura para centralização via CSS).
- **Critério de validação:** `tests/frontend-bootstrap/test_home_page.py::test_home_displays_only_funcionou` passa.
- **Estimativa:** S
- **Bloqueadores:** T-004

### T-006 — Centralização via flexbox nativo em globals.css

- **Objetivo:** Centralizar horizontal e verticalmente o conteúdo da home usando apenas CSS nativo.
- **Input:** `app/globals.css` limpo da T-003.
- **Output:** `app/globals.css` com reset mínimo, `body` ou `main` com `min-height: 100vh`, `display: flex`, `align-items: center`, `justify-content: center`, `margin: 0`, cor de texto escura sobre fundo claro garantindo contraste.
- **Critério de validação:** `tests/frontend-bootstrap/test_home_page.py::test_funcionou_is_centered` passa.
- **Estimativa:** S
- **Bloqueadores:** T-005

### T-007 — README com instruções de uso

- **Objetivo:** Documentar pré-requisitos, instalação, dev, build e estrutura.
- **Input:** Projeto funcional.
- **Output:** `README.md` na raiz com seções: Pré-requisitos (Node 20 LTS via nvm, pnpm), Instalação (`pnpm install`), Desenvolvimento (`pnpm dev`), Build (`pnpm build`), Estrutura de pastas.
- **Critério de validação:** `tests/frontend-bootstrap/test_repository_structure.py::test_repo_has_minimum_structure` passa (verifica existência + keywords mínimas no README).
- **Estimativa:** S
- **Bloqueadores:** T-006

### T-008 — Validação smoke: dev server e build

- **Objetivo:** Confirmar que `pnpm dev` sobe sem erros e `pnpm build` finaliza com exit 0.
- **Input:** Projeto completo das T-001 a T-007.
- **Output:** Execução bem-sucedida de `pnpm install`, `pnpm dev` (servidor disponível em `localhost:3000` renderizando "funcionou" centralizado) e `pnpm build` (exit 0, sem warnings críticos).
- **Critério de validação:** `tests/frontend-bootstrap/test_dev_server.py::test_dev_server_starts_without_errors`, `test_dev_server.py::test_error_without_node_modules` e `tests/frontend-bootstrap/test_build.py::test_production_build_succeeds` passam.
- **Estimativa:** S
- **Bloqueadores:** T-007

---

## Progress ledger (espelho leve do Convex)

| ID | Status | Owner | Iniciada | Concluída |
|----|--------|-------|----------|-----------|
| T-001 | pending | — | — | — |
| T-002 | pending | — | — | — |
| T-003 | pending | — | — | — |
| T-004 | pending | — | — | — |
| T-005 | pending | — | — | — |
| T-006 | pending | — | — | — |
| T-007 | pending | — | — | — |
| T-008 | pending | — | — | — |

> O progress ledger autoritativo está em `progress_ledger` no Convex. Esta tabela é espelho legível por humano.

---

**EM Agent:** em-agent-v1
**Próximo passo:** QA/Test Agent escreve testes derivados de `acceptance.md` (CURRANTE: red antes de Implementation começar).
