# JSAAI — Frontend Bootstrap

Boostrap do projeto React com Next.js 15 + React 19 + TypeScript.

## Pré-requisitos

- Node.js 20 LTS (use [nvm](https://github.com/nvm-sh/nvm): `nvm use`)
- [pnpm](https://pnpm.io/) (`npm install -g pnpm`)

## Instalação

```bash
pnpm install
```

## Desenvolvimento

```bash
pnpm dev
```

Acesse [http://localhost:3000](http://localhost:3000) no navegador.

Para usar outra porta:

```bash
PORT=3001 pnpm dev
```

## Build de produção

```bash
pnpm build
```

Os arquivos gerados ficam em `.next/`.

## Iniciar servidor de produção

```bash
pnpm start
```

## Estrutura de pastas

```
.
├── src/
│   └── app/
│       ├── globals.css   # estilos globais e centralização
│       ├── layout.tsx    # root layout
│       └── page.tsx      # página inicial
├── public/               # assets estáticos
├── package.json
├── tsconfig.json
├── next.config.ts
└── README.md
```
