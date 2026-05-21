# spec.md — 003-react-bootstrap-home

> **Light Spec** — marcar uma.
> Esta spec é a fonte de verdade da feature. Código que diverge é bug, não criatividade.

## Objetivo

Inicializar o projeto React no repositório vazio e publicar uma página inicial funcional exibindo a mensagem "funcionou" centralizada, validando assim o pipeline de desenvolvimento end-to-end.

## Escopo

- Inicializar estrutura padrão de projeto React no repositório.
- Configurar script de execução local (`dev`) e script de build de produção.
- Criar página inicial (home) com fundo branco (ou padrão do framework), exibindo exclusivamente o texto "funcionou" centralizado vertical e horizontalmente, sem dependências extras de UI.
- Adicionar `README.md` com instruções mínimas de execução (instalação de dependências, comando dev, comando build).

## Fora de escopo

- Autenticação e controle de acesso.
- Integração com API ou backend.
- Design system ou biblioteca de componentes de UI.
- Testes avançados ou E2E.
- Roteamento além da página inicial.
- Deploy automatizado em ambiente de produção.

## Requisitos funcionais

| ID | Requisito | Origem |
|----|-----------|--------|
| RF-001 | O repositório deve conter uma estrutura de projeto React inicializada (package.json, src/, public/ ou equivalente). | Issue #3 |
| RF-002 | Deve existir um script `dev` (ou equivalente) que inicie o servidor de desenvolvimento local sem erros. | Issue #3 |
| RF-003 | Deve existir um script `build` que gere o bundle de produção sem erros. | Issue #3 |
| RF-004 | A página inicial deve exibir única e exclusivamente o texto "funcionou" visível ao usuário. | Issue #3 |
| RF-005 | O texto "funcionou" deve estar centralizado vertical e horizontalmente na viewport. | Issue #3 |
| RF-006 | O estilo da página deve ser simples, sem dependências externas de UI (ex: sem Material UI, Tailwind, Bootstrap). | Issue #3 |
| RF-007 | O repositório deve conter um `README.md` com instruções de instalação e execução local. | Issue #3 |

## Requisitos não-funcionais

| ID | Requisito | Limite mensurável |
|----|-----------|-------------------|
| RNF-001 | Tempo de inicialização do servidor de desenvolvimento | Menos de 30 segundos em hardware padrão de desenvolvimento |
| RNF-002 | Tamanho do bundle de produção (JS principal) | [QUESTION: há limite definido para o bundle inicial? Sugestão: < 200 KB gzipped para uma página trivial] |

## Restrições e regulação aplicável

Criticidade lv1_light. Nenhuma regulação específica (LGPD, BACEN, OAB) é aplicável a este bootstrap de frontend estático sem dados de usuário ou backend. Não há coleta, processamento ou armazenamento de dados pessoais nesta feature.

## Contratos públicos afetados

Nenhum contrato de API, schema ou evento é criado ou alterado por esta feature. Trata-se exclusivamente de frontend estático.

| Contrato | Tipo | Mudança | Versão antes → depois |
|----------|------|---------|------------------------|
| N/A | — | — | — |

## Casos de erro previstos

| Caso | Comportamento esperado | HTTP / código de erro |
|------|------------------------|-----------------------|
| Dependências não instaladas ao rodar `dev` | O terminal exibe mensagem de erro clara indicando ausência de `node_modules`; o servidor não sobe | Erro de processo (exit code != 0) |
| Porta padrão ocupada | [QUESTION: o projeto deve configurar fallback de porta automático ou apenas documentar no README?] | Erro de processo |

## Requisitos de segurança

Feature lv1_light sem input de usuário, sem autenticação, sem dados sensíveis e sem comunicação com backend. Não há boundary de privilégio relevante. Nenhum threat model adicional é necessário além das boas práticas padrão:
- Não commitar arquivos `.env` ou segredos no repositório.
- `.gitignore` deve excluir `node_modules/` e arquivos de build gerados.

## Critérios de aceite

Ver `acceptance.md` (cenários BDD).

## Riscos identificados

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|----------|
| Versão do Node.js incompatível no ambiente de desenvolvimento | baixa | baixo | Documentar versão mínima de Node no README; considerar `.nvmrc` |
| Conflito de porta padrão (ex: 3000 já em uso) | baixa | baixo | Documentar como trocar a porta no README |

---

**Criticidade:** Light
**HITL gate:** none
**Bounded context:** `frontend-bootstrap`
**Issue GitHub:** #3
**Mantenedor desta spec:** Product Analyst Agent (revisada por humano accountable)
