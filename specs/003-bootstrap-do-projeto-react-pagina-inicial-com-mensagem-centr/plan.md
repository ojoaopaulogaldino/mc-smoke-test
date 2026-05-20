# plan.md — 003-react-bootstrap-home

> Plano técnico. Como vamos implementar a `spec.md`.
> Architect Agent escreve. Implementation Agent consome.

## Sequência técnica

1. Inicializar projeto Next.js 15 + React 19 + TypeScript 5.x na raiz do repositório usando `pnpm create next-app@latest . --typescript --app --no-tailwind --no-eslint --no-src-dir --import-alias '@/*'` (commit: `chore: bootstrap next.js 15 + react 19 project`).
2. Fixar versão do Node.js criando `.nvmrc` com Node 20 LTS e ajustar `engines` no `package.json` (commit: `chore: pin node version to 20 LTS`).
3. Limpar arquivos boilerplate gerados pelo Next (favicon padrão pode ficar, mas remover conteúdo demo de `app/page.tsx` e estilos demo em `app/globals.css`) (commit: `chore: remove next.js boilerplate content`).
4. Implementar `app/page.tsx` como Server Component renderizando apenas a string `funcionou` dentro de um `<main>` com classe CSS para centralização (commit: `feat(frontend-bootstrap): render funcionou message on home`).
5. Implementar centralização em `app/globals.css` usando flexbox nativo no `body` ou `main` (sem libs externas), com `min-height: 100vh`, `display: flex`, `align-items: center`, `justify-content: center`, garantindo contraste texto-escuro / fundo-branco (commit: `style(frontend-bootstrap): center funcionou using native flexbox`).
6. Ajustar `app/layout.tsx` com `<html lang="pt-BR">`, metadata mínima (`title: 'JSAAI'`, descrição neutra), e remover fontes/decoração demo (commit: `chore: minimal root layout`).
7. Escrever `README.md` na raiz com seções: Pré-requisitos (Node 20 LTS via nvm, pnpm), Instalação (`pnpm install`), Desenvolvimento (`pnpm dev`), Build (`pnpm build`), Estrutura de pastas (commit: `docs: add README with run instructions`).
8. Validar localmente: `pnpm install`, `pnpm dev` → abre em `http://localhost:3000`, vê "funcionou" centralizado; `pnpm build` finaliza com exit 0 e sem warnings críticos (commit: nenhum, apenas validação).
9. Garantir que `package.json` final NÃO contém libs de UI externas (Material UI, Chakra, AntD, Bootstrap, Tailwind nesta entrega) — apenas `next`, `react`, `react-dom` e `@types/*` em devDependencies.

## Arquivos prováveis

| Arquivo | Mudança esperada |
|---------|-------------------|
| `package.json` | criar (gerado pelo `create-next-app`, depois ajustado) |
| `pnpm-lock.yaml` | criar |
| `tsconfig.json` | criar (gerado) |
| `next.config.ts` | criar (default) |
| `.nvmrc` | criar (conteúdo: `20`) |
| `.gitignore` | criar (gerado pelo Next) |
| `app/layout.tsx` | criar (root layout minimal, `lang=pt-BR`) |
| `app/page.tsx` | criar (renderiza "funcionou") |
| `app/globals.css` | criar (reset minimal + centralização flex) |
| `README.md` | criar (instruções dev/build) |
| `public/` | criar (pasta padrão Next, vazia ou com favicon default) |

## ADRs vinculadas

**Sem ADR — uso de padrões já estabelecidos.**

A constituição da JSAAI já manda Next.js 15 + React 19 + TypeScript 5.x + pnpm como stack de frontend. Esta feature apenas materializa o padrão existente sem trade-off arquitetural não-óbvio, sem novo contrato público, sem nova dependência externa e sem nova política. Não há decisão que mereça ADR.

## Plano de testes (alto nível)

Estratégia: como é bootstrap puro de frontend sem lógica de domínio, os testes derivados de `acceptance.md` são majoritariamente smoke/integration (build + inspeção estática + render). QA Agent vai converter os arquivos `tests/frontend-bootstrap/test_*.py` listados no acceptance em testes executáveis. Aceita-se que os "testes" sejam scripts pytest que invocam comandos npm/pnpm via subprocess e parseiam saída + parseiam HTML renderizado (não há Python de produção neste contexto).

- **Unit:** N/A (nenhuma lógica de domínio).
- **Integration:** validar `pnpm dev` sobe sem erros (CA-001, CA-007); validar `pnpm build` finaliza exit 0 (CA-004). Executar via `subprocess` em pytest.
- **E2E:** validar render da home — pode ser feito com Playwright headless OU simplesmente fazendo `curl http://localhost:3000` durante o dev server e parseando o HTML em busca da string exata "funcionou" (CA-002). Centralização (CA-003) pode ser validada por inspeção dos estilos computados via Playwright, ou aceita como inspeção do CSS-fonte se Playwright for overkill para Lv.1.
- **Contract:** N/A (sem APIs, schemas ou eventos).
- **Estrutura:** validar via `os.path.exists` + parse de `package.json` que (a) `README.md` existe e contém keywords mínimas, (b) `package.json` existe, (c) pasta `app/` existe com `page.tsx`, (d) nenhuma dep proibida de UI lib externa está em `dependencies`/`devDependencies` (CA-005, CA-006).

## Plano de observabilidade

Feature de bootstrap puramente local, sem runtime de produção nesta entrega (deploy está fora de escopo na spec). Observabilidade de runtime não se aplica.

Sinais relevantes ainda assim, no nível CI/local:

| Sinal | Tipo | Onde | Threshold |
|-------|------|------|-----------|
| `pnpm_build_exit_code` | gauge (CI) | pipeline | alerta se != 0 |
| `pnpm_build_duration_seconds` | gauge (CI) | pipeline | informativo; alerta se > 120s |
| `pnpm_dev_startup_seconds` | gauge (teste local) | smoke test | alerta se > 30s (RNF-001) |

Quando a feature de deploy entrar (fora desta spec), uma nova plan vai adicionar métricas runtime (request_total, latency, error). Aqui, basta o gate de CI.

## Plano de rollback

Criticidade Lv.1 e repositório vazio antes desta feature. Rollback é trivial: `git revert` do merge commit OU `git reset` para o estado anterior (repo vazio). Não há dados persistidos, não há usuários ativos, não há deploy.

- Como reverter código: `git revert <merge_sha>` no `main`.
- Como reverter dados: N/A.
- Janela de detecção: N/A (sem produção).
- Sinais que disparam rollback: falha no `pnpm build` na CI pós-merge.

## Riscos técnicos

| Risco | Mitigação |
|-------|-----------|
| Next.js 15 + React 19 ainda têm peer-deps com versões instáveis em libs do ecossistema | manter `dependencies` mínimas (só `next`, `react`, `react-dom`) nesta entrega, evitando conflitos |
| Desenvolvedor com Node antigo não consegue rodar | `.nvmrc` + seção "Pré-requisitos" explícita no README com comando `nvm use` |
| Conteúdo de "funcionou" cair em página com fontes/decoração default invisível | CSS explícito em `globals.css` define `color`, `font-size`, `background`, garantindo contraste; CA-003 verifica visibilidade |
| `create-next-app` adicionar Tailwind ou ESLint por default em versão futura, contradizendo CA-006 | flags `--no-tailwind --no-eslint` explícitas no comando de bootstrap; checar `package.json` final manualmente antes do commit |
| Servidor dev demorar > 30s violando RNF-001 em máquinas modestas | aceitável como informativo; primeira execução pode ter cold start de turbopack — documentar no README |

---

**Architect Agent:** architect-agent-v1
**Reviewed by:** N/A (HITL: none)
**Próximo passo:** EM decompõe em `tasks.md`.
