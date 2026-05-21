# JSAAI Frontend

Projeto React/Next.js com página inicial exibindo "funcionou".

## Pré-requisitos

- Node.js 20 LTS (use [nvm](https://github.com/nvm-sh/nvm): `nvm use`)
- [pnpm](https://pnpm.io/) (`npm install -g pnpm`)

## Instalação

Instale as dependências:

```bash
pnpm install
```

## Desenvolvimento

Inicie o servidor de desenvolvimento:

```bash
pnpm dev
```

Acesse [http://localhost:3000](http://localhost:3000) no navegador.

Para usar uma porta diferente:

```bash
PORT=3001 pnpm dev
```

## Build de produção

Gere o bundle de produção:

```bash
pnpm build
```

Inicie o servidor de produção:

```bash
pnpm start
```

## Estrutura de pastas

```
.
├── src/
│   └── app/
│       ├── globals.css    # Estilos globais com centralização
│       ├── layout.tsx     # Layout raiz
│       └── page.tsx       # Página inicial
├── public/                # Arquivos estáticos
├── .gitignore
├── .nvmrc                 # Node 20 LTS
├── next.config.ts
├── package.json
├── README.md
└── tsconfig.json
```
