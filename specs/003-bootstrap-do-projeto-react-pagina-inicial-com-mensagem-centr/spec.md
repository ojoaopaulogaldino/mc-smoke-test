# spec.md — 003-react-bootstrap-home

> **Light Spec** — marcar uma.
> Esta spec é a fonte de verdade da feature. Código que diverge é bug, não criatividade.

## Objetivo

Inicializar o projeto React no repositório vazio e publicar uma página home funcional exibindo a mensagem "funcionou" centralizada, validando que o pipeline de desenvolvimento está operacional.

## Escopo

- Inicializar projeto React com estrutura padrão (ex: Create React App, Vite ou equivalente).
- Configurar script de execução local (`dev` ou `start`) e script de build de produção (`build`).
- Criar página inicial (`/`) com fundo branco (ou padrão do framework), exibindo o texto "funcionou" centralizado vertical e horizontalmente, sem dependências extras de UI.
- Adicionar `README.md` na raiz com instruções mínimas de como executar o projeto localmente e realizar o build.

## Fora de escopo

- Autenticação e autorização.
- Integração com API ou backend.
- Design system ou biblioteca de componentes de UI (ex: Material UI, Chakra, etc.).
- Testes avançados ou E2E.
- Roteamento além da página inicial.
- Deploy/publicação em ambiente de produção ou staging.

## Requisitos funcionais

| ID | Requisito | Origem |
|----|-----------|--------|
| RF-001 | O projeto deve inicializar e executar via comando de desenvolvimento (ex: `npm run dev` ou `npm start`) sem erros de compilação ou runtime. | Issue #3 |
| RF-002 | Ao acessar a URL raiz (`/`) da aplicação em execução local, o único conteúdo textual visível deve ser a mensagem exata "funcionou". | Issue #3 |
| RF-003 | A mensagem "funcionou" deve estar centralizada tanto verticalmente quanto horizontalmente na viewport. | Issue #3 |
| RF-004 | O estilo de centralização deve ser implementado sem dependências externas de UI (apenas CSS nativo ou CSS-in-JS básico do framework). | Issue #3 |
| RF-005 | O comando de build de produção (ex: `npm run build`) deve executar com sucesso, gerando artefatos sem erros. | Issue #3 |
| RF-006 | O repositório deve conter um `README.md` com instruções claras de como instalar dependências, executar localmente e realizar o build. | Issue #3 |
| RF-007 | A estrutura de arquivos do projeto deve seguir a organização padrão do toolchain escolhido. | Issue #3 |

## Requisitos não-funcionais

| ID | Requisito | Limite mensurável |
|----|-----------|-------------------|
| RNF-001 | Tempo de inicialização do servidor de desenvolvimento | < 30s em máquina de desenvolvimento padrão |
| RNF-002 | Tempo de carregamento da página home em dev | < 3s no browser local |
| RNF-003 | Build de produção sem warnings críticos | 0 erros de build |

## Restrições e regulação aplicável

Feature de bootstrap de projeto frontend sem coleta de dados pessoais, sem autenticação e sem integração externa. Não há itens regulatórios (LGPD, BACEN, OAB) aplicáveis neste escopo.

[QUESTION: A constituição da empresa jsaai define algum toolchain obrigatório para projetos React (ex: Vite vs CRA vs Next.js)? Caso sim, o RF-001 deve ser atualizado para refletir o toolchain mandatório.]

## Contratos públicos afetados

Nenhum. Esta feature não expõe APIs, schemas ou eventos. É exclusivamente frontend estático.

| Contrato | Tipo | Mudança | Versão antes → depois |
|----------|------|---------|------------------------|
| — | — | Não aplicável | — |

## Casos de erro previstos

| Caso | Comportamento esperado | HTTP / código de erro |
|------|------------------------|-----------------------|
| Dependências não instaladas ao rodar `dev` | Terminal exibe erro claro de módulo não encontrado; o README deve instruir `npm install` antes de `npm run dev` | N/A (erro de CLI) |
| Versão incompatível de Node.js | Ferramenta de build exibe mensagem de versão mínima requerida | N/A (erro de CLI) |
| Acesso a rota inexistente (ex: `/qualquer-coisa`) | [QUESTION: Deve exibir 404 customizado ou redirecionar para home? Por ora, comportamento padrão do toolchain é aceitável.] | N/A (SPA local) |

## Requisitos de segurança

Criticidade lv1_light, sem dados sensíveis, sem autenticação, sem input de usuário e sem integração externa. Nenhum threat model é necessário neste escopo.

## Critérios de aceite

Ver `acceptance.md` (cenários BDD).

## Riscos identificados

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Toolchain escolhido deprecado ou com conflito de versão do Node | baixa | baixo | Fixar versão do Node no `README.md` e/ou `.nvmrc` |
| Texto "funcionou" renderizado mas não visível por sobreposição de estilos padrão | baixa | baixo | Verificar contraste (texto escuro em fundo branco) no CA de aceite |

---

**Criticidade:** Light
**HITL gate:** none
**Bounded context:** `frontend-bootstrap`
**Issue GitHub:** #3
**Mantenedor desta spec:** Product Analyst Agent (revisada por humano accountable)
