# acceptance.md — 003-react-bootstrap-home

> Cenários de aceite em formato BDD (Dado / Quando / Então).
> Cada cenário tem ID. QA/Test Agent deriva um teste por cenário (CURRANTE).
> Spec coverage gate calcula: (CAs cobertos por teste passando) / (CAs total).

## Cenários

### CA-001 — Servidor de desenvolvimento inicia sem erros

**Dado** que as dependências do projeto estão instaladas (`npm install` ou equivalente executado com sucesso)
**Quando** o comando de desenvolvimento (`npm run dev` ou equivalente) é executado
**Então** o servidor local sobe sem erros no terminal
**E** uma URL local acessível é exibida no terminal (ex: `http://localhost:3000` ou equivalente)

### CA-002 — Página inicial exibe apenas o texto "funcionou"

**Dado** que o servidor de desenvolvimento está rodando
**Quando** o usuário acessa a URL local da aplicação no navegador
**Então** a única mensagem visível na página é o texto exato "funcionou"
**E** nenhum outro conteúdo de texto ou elemento visual proeminente é exibido além dessa mensagem

### CA-003 — Texto "funcionou" está centralizado na viewport

**Dado** que o servidor de desenvolvimento está rodando
**Quando** o usuário acessa a URL local da aplicação no navegador com viewport padrão (desktop)
**Então** o texto "funcionou" está posicionado no centro horizontal da tela
**E** o texto "funcionou" está posicionado no centro vertical da tela

### CA-004 — Build de produção executa sem erros

**Dado** que as dependências do projeto estão instaladas
**Quando** o comando de build (`npm run build` ou equivalente) é executado
**Então** o processo finaliza com código de saída 0 (sucesso)
**E** os arquivos de bundle são gerados no diretório de saída (ex: `dist/` ou `build/`)

### CA-005 — Repositório contém estrutura mínima organizada

**Dado** que o repositório foi clonado
**Quando** o conteúdo do repositório é inspecionado
**Então** existe um arquivo `package.json` na raiz
**E** existe um diretório `src/` (ou equivalente) contendo o código-fonte React
**E** existe um arquivo `README.md` na raiz
**E** existe um arquivo `.gitignore` que inclui `node_modules/`

### CA-006 — README contém instruções de execução

**Dado** que o repositório foi clonado
**Quando** o arquivo `README.md` é lido
**Então** o arquivo contém instruções para instalar as dependências
**E** o arquivo contém o comando para iniciar o servidor de desenvolvimento
**E** o arquivo contém o comando para executar o build de produção

### CA-007 — Caso de erro: dependências não instaladas

**Dado** que o diretório `node_modules/` não existe (dependências não instaladas)
**Quando** o comando de desenvolvimento é executado
**Então** o processo falha com código de saída diferente de 0
**E** uma mensagem de erro é exibida no terminal indicando o problema

---

## Mapeamento CA → teste

Atualizado pelo QA/Test Agent ao escrever os testes (CURRANTE: red).
Atualizado pelo QA Agent ao validar (green + edge cases).

| CA | Arquivo de teste | Test function | Status |
|----|------------------|---------------|--------|
| CA-001 | `tests/frontend-bootstrap/test_bootstrap.py` | `test_dev_server_starts_without_errors` | red |
| CA-002 | `tests/frontend-bootstrap/test_bootstrap.py` | `test_home_displays_only_funcionou_text` | red |
| CA-003 | `tests/frontend-bootstrap/test_bootstrap.py` | `test_funcionou_text_is_centered` | red |
| CA-004 | `tests/frontend-bootstrap/test_bootstrap.py` | `test_production_build_succeeds` | red |
| CA-005 | `tests/frontend-bootstrap/test_bootstrap.py` | `test_repository_has_minimum_structure` | red |
| CA-006 | `tests/frontend-bootstrap/test_bootstrap.py` | `test_readme_contains_execution_instructions` | red |
| CA-007 | `tests/frontend-bootstrap/test_bootstrap.py` | `test_dev_command_fails_without_node_modules` | red |

---

**Product Analyst Agent:** product-analyst-agent-v1
**Última revisão humana (se Lv.3):** N/A (HITL: none)
