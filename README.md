# JSAAI Frontend

Página inicial do projeto JSAAI.

## Pré-requisitos

- Node.js 20 LTS (recomendado via [nvm](https://github.com/nvm-sh/nvm))
- [pnpm](https://pnpm.io/) (gerenciador de pacotes)

```bash
nvm use 20
npm install -g pnpm
```

## Instalação

Instale as dependências do projeto:

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
│       ├── layout.tsx   # Layout raiz (html, body, metadata)
│       ├── page.tsx     # Página inicial
│       └── globals.css  # Estilos globais (reset + centralização)
├── public/              # Assets estáticos
├── package.json
├── tsconfig.json
├── next.config.ts
├── .nvmrc               # Node 20 LTS
├── .gitignore
└── README.md
```
