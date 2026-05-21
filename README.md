# JSAAI Frontend Bootstrap

Projeto React com Next.js 15 e React 19.

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
│       ├── globals.css   # Estilos globais
│       ├── layout.tsx    # Layout raiz
│       └── page.tsx      # Página inicial
├── public/               # Arquivos estáticos
├── .gitignore
├── .nvmrc
├── next.config.ts
├── package.json
├── README.md
└── tsconfig.json
```

## Troca de porta

Caso a porta 3000 esteja ocupada:

```bash
PORT=3001 pnpm dev
```
