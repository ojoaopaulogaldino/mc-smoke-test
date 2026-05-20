# plan.md — 003-react-bootstrap-home

> Plano técnico. Como vamos implementar a `spec.md`.
> Architect Agent escreve. Implementation Agent consome.

## Sequência técnica

1. Inicializar projeto Next.js 15 + React 19 + TypeScript usando `pnpm create next-app@latest` na raiz do repositório, com configuração: App Router habilitado, TypeScript, sem Tailwind (RF-006 proíbe lib de UI), sem ESLint customizado além do default, src directory habilitado, import alias `@/*`.
2. Adicionar `.nvmrc` fixando Node 20 LTS (compatível com Next 15 + React 19) e ajustar `.gitignore` para garantir exclusão de `node_modules/`, `.next/`, `out/`, `.env*` (validação contra requisito de segurança da spec).
3. Substituir conteúdo da página inicial (`src/app/page.tsx`) por componente que renderiza apenas o texto "funcionou", removendo qualquer boilerplate do template (logos, links, instruções).
4. Substituir/criar `src/app/globals.css` com reset mínimo (margin/padding zero em `html, body`) e estilos para centralizar o texto vertical+horizontalmente via flexbox em container de altura `100vh` (RF-005). Remover qualquer CSS supérfluo do template.
5. Ajustar `src/app/layout.tsx` para metadata mínima (title: "funcionou") e remover fontes customizadas/Google Fonts do boilerplate, mantendo dependência zero de UI externa.
6. Escrever `README.md` na raiz com: pré-requisitos (Node 20+, pnpm), comandos `pnpm install`, `pnpm dev`, `pnpm build`, `pnpm start`, e nota sobre troca de porta (`PORT=3001 pnpm dev`) cobrindo CA-006 e mitigação de risco de porta ocupada.
7. Validar localmente: `pnpm install` → `pnpm dev` sobe sem erro → acessar `http://localhost:3000` mostra "funcionou" centralizado → `pnpm build` finaliza com exit 0 → bundle inicial inspecionado.
8. Commit único (Lv.1) ou sequência curta de commits seguindo ordem acima; abrir PR vinculado à issue #3.

## Arquivos prováveis

| Arquivo | Mudança esperada |
|---------|-------------------|
| `package.json` | criar (gerado pelo create-next-app, ajustar scripts se necessário) |
| `pnpm-lock.yaml` | criar |
| `tsconfig.json` | criar (default Next.js) |
| `next.config.ts` | criar (default Next.js) |
| `src/app/page.tsx` | criar — renderiza apenas "funcionou" |
| `src/app/layout.tsx` | criar — layout mínimo, sem fontes externas |
| `src/app/globals.css` | criar — reset + centralização flexbox |
| `public/` | criar (vazio ou apenas favicon default) |
| `README.md` | criar — instruções de execução |
| `.gitignore` | criar/ajustar — `node_modules/`, `.next/`, `out/`, `.env*` |
| `.nvmrc` | criar — `20` |

## ADRs vinculadas

**Sem ADR — uso de padrões já estabelecidos.**

Next.js 15 + React 19 + pnpm já são stack mandatória pela constituição JSAAI (seção 2). Nenhum contrato público, invariante arquitetural novo, trade-off não-óbvio ou dependência externa nova é introduzido. Bootstrap trivial de frontend.

## Plano de testes (alto nível)

O `acceptance.md` mapeia CAs para `tests/frontend-bootstrap/test_bootstrap.py` (pytest). Como o stack é TS/Next, os testes serão de natureza estrutural/processual (subprocess + filesystem + HTTP), apropriados para validar bootstrap.

- **Unit:** não aplicável (não há lógica de domínio).
- **Integration (estrutural):** verificar presença de arquivos-chave (`package.json`, `src/app/page.tsx`, `README.md`, `.gitignore`) — CA-005, CA-006.
- **Integration (processual):** rodar `pnpm install` + `pnpm dev` via subprocess, validar que servidor sobe em <30s e responde HTTP 200 com texto "funcionou" — CA-001, CA-002.
- **Integration (build):** rodar `pnpm build` via subprocess e validar exit code 0 + presença de `.next/` — CA-004.
- **Integration (erro):** rodar `pnpm dev` sem `node_modules/` e validar exit code != 0 — CA-007.
- **Visual/posicionamento:** CA-003 (centralização) validado via inspeção de CSS gerado ou snapshot do HTML servido, checando presença das regras flexbox no `globals.css` aplicado ao container.
- **E2E:** não aplicável (sem fluxo de usuário complexo).
- **Contract:** não aplicável (sem API).

## Plano de observabilidade

Feature lv1_light de bootstrap estático sem runtime de produção neste momento. Observabilidade de produção fora do escopo.

| Sinal | Tipo | Onde | Threshold |
|-------|------|------|-----------|
| build success/failure | CI signal | GitHub Actions (quando configurado) | falha em main → bloqueia merge |
| dev server startup time | manual (README) | local | < 30s (RNF-001) |

Nenhuma métrica de runtime (counter/histogram) é instrumentada nesta entrega — não há backend nem tráfego de usuário real.

## Plano de rollback

Criticidade lv1_light. Rollback padrão pelo pipeline Git:

- Como reverter código: `git revert <SHA do merge>` na branch `main` + novo PR.
- Como reverter dados: N/A (sem persistência, sem migration).
- Janela de detecção: imediata (feature roda localmente; sem deploy de produção neste PR).
- Sinais que disparam rollback: falha de `pnpm install` / `pnpm dev` / `pnpm build` em ambiente limpo reportada por outro dev.

## Riscos técnicos

| Risco | Mitigação |
|-------|-----------|
| Incompatibilidade React 19 + libs auxiliares do template Next 15 (ainda em estabilização) | Usar template oficial mais recente do `create-next-app`; fixar versões no `package.json` gerado; não adicionar libs além das default |
| Boilerplate do `create-next-app` deixa resíduos (logos, links, CSS extra) que violam RF-004 ("única mensagem visível") | Passo 3-5 explicitamente limpa `page.tsx`, `layout.tsx`, `globals.css`; revisor do PR confere visualmente |
| Fontes do Google (next/font) adicionadas pelo template podem ser interpretadas como "dependência externa de UI" (RF-006) | Remover `next/font` do `layout.tsx`; usar `font-family: system-ui, sans-serif` no CSS |
| Bundle size do Next 15 vazio pode exceder sugestão de 200 KB gzipped (RNF-002 com [QUESTION]) | RNF-002 está marcado como QUESTION na spec; documentar tamanho real medido no PR e seguir adiante (não é gate) |
| Testes pytest rodando `pnpm` via subprocess podem ser frágeis em CI sem Node instalado | Documentar pré-requisito no QA setup; QA Agent decide se mocka ou exige Node no runner |

---

**Architect Agent:** architect-agent-v1
**Reviewed by:** N/A (HITL: none)
**Próximo passo:** EM decompõe em `tasks.md`.
