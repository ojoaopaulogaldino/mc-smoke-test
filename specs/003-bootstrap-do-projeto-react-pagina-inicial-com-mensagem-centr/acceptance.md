# acceptance.md — 003-react-bootstrap-home

> Cenários de aceite em formato BDD (Dado / Quando / Então).
> Cada cenário tem ID. QA/Test Agent deriva um teste por cenário (CURRANTE).
> Spec coverage gate calcula: (CAs cobertos por teste passando) / (CAs total).

## Cenários

### CA-001 — Servidor de desenvolvimento inicia sem erros

**Dado** que as dependências do projeto foram instaladas (`npm install` ou equivalente executado com sucesso)
**E** que o ambiente possui versão de Node.js compatível com o toolchain do projeto
**Quando** o comando de desenvolvimento é executado (ex: `npm run dev` ou `npm start`)
**Então** o servidor local sobe sem erros de compilação ou runtime no terminal
**E** uma URL local (ex: `http://localhost:3000` ou `http://localhost:5173`) fica disponível para acesso

---

### CA-002 — Página home exibe exclusivamente a mensagem "funcionou"

**Dado** que o servidor de desenvolvimento está em execução
**Quando** o usuário acessa a URL raiz (`/`) no browser
**Então** a página renderiza e o único conteúdo textual visível na tela é a string exata `funcionou`
**E** nenhum outro texto, placeholder ou mensagem padrão do framework é exibido na viewport

---

### CA-003 — Mensagem "funcionou" está centralizada na viewport

**Dado** que o servidor de desenvolvimento está em execução
**Quando** o usuário acessa a URL raiz (`/`) no browser com viewport padrão (ex: 1280x720)
**Então** o elemento que contém o texto "funcionou" está posicionado no centro horizontal da página
**E** o elemento que contém o texto "funcionou" está posicionado no centro vertical da página

---

### CA-004 — Build de produção executa sem erros

**Dado** que as dependências do projeto estão instaladas
**Quando** o comando de build de produção é executado (ex: `npm run build`)
**Então** o processo finaliza com código de saída `0` (sucesso)
**E** uma pasta de artefatos de build é gerada no diretório esperado (ex: `dist/` ou `build/`)
**E** nenhum erro crítico é reportado no output do terminal

---

### CA-005 — Repositório contém estrutura mínima organizada

**Dado** que o repositório foi clonado
**Quando** o conteúdo da raiz do repositório é inspecionado
**Então** existe um arquivo `README.md` na raiz
**E** o `README.md` contém instruções de como instalar dependências, executar localmente e realizar o build
**E** existe um arquivo de configuração de projeto (ex: `package.json`) na raiz
**E** existe uma pasta de código-fonte (ex: `src/`) com pelo menos um componente ou arquivo de entrada

---

### CA-006 — Centralização não depende de biblioteca externa de UI

**Dado** que o projeto foi inicializado
**Quando** o arquivo `package.json` é inspecionado
**Então** não há dependências de bibliotecas de UI externas (ex: Material UI, Chakra UI, Ant Design, Bootstrap) listadas em `dependencies` ou `devDependencies`

---

### CA-007 — Caso de erro: execução sem instalação de dependências

**Dado** que as dependências NÃO foram instaladas (pasta `node_modules` ausente)
**Quando** o comando de desenvolvimento é executado
**Então** o terminal exibe uma mensagem de erro clara indicando módulo não encontrado ou dependências ausentes
**E** o processo não entra em estado de execução silenciosamente corrompido

---

## Mapeamento CA → teste

Atualizado pelo QA/Test Agent ao escrever os testes (CURRANTE: red).
Atualizado pelo QA Agent ao validar (green + edge cases).

| CA | Arquivo de teste | Test function | Status |
|----|------------------|-----------------|--------|
| CA-001 | `tests/frontend-bootstrap/test_dev_server.py` | `test_dev_server_starts_without_errors` | red |
| CA-002 | `tests/frontend-bootstrap/test_home_page.py` | `test_home_displays_only_funcionou` | red |
| CA-003 | `tests/frontend-bootstrap/test_home_page.py` | `test_funcionou_is_centered` | red |
| CA-004 | `tests/frontend-bootstrap/test_build.py` | `test_production_build_succeeds` | red |
| CA-005 | `tests/frontend-bootstrap/test_repository_structure.py` | `test_repo_has_minimum_structure` | red |
| CA-006 | `tests/frontend-bootstrap/test_repository_structure.py` | `test_no_external_ui_library_dependency` | red |
| CA-007 | `tests/frontend-bootstrap/test_dev_server.py` | `test_error_without_node_modules` | red |

---

**Product Analyst Agent:** product-analyst-agent-v1
**Última revisão humana (se Lv.3):** N/A (HITL: none)
