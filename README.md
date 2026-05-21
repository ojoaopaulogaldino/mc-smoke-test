# JSAAI — Frontend Bootstrap

Página inicial com mensagem "funcionou" centralizada.

## Pré-requisitos

- Node.js 20 LTS (recomendado via [nvm](https://github.com/nvm-sh/nvm))
- [pnpm](https://pnpm.io/) instalado globalmente

```bash
nvm use 20
npm install -g pnpm
```

## Instalação

```bash
pnpm install
```

## Desenvolvimento

```bash
pnpm dev
```

Abra [http://localhost:3000](http://localhost:3000) no navegador.

## Build de produção

```bash
pnpm build
```

Os arquivos de bundle são gerados no diretório `.next/`.

## Iniciar servidor de produção

```bash
pnpm start
```

## Estrutura de pastas

```
├── src/
│   └── app/
│       ├── globals.css   # Reset CSS + centralização flexbox
│       ├── layout.tsx    # Root layout (pt-BR, metadata mínima)
│       └── page.tsx      # Página inicial — exibe "funcionou"
├── public/               # Assets estáticos
├── .gitignore
├── .nvmrc                # Node 20 LTS
├── next.config.ts
├── package.json
├── README.md
└── tsconfig.json
```

## Nota sobre porta

Caso a porta 3000 esteja ocupada:

```bash
PORT=3001 pnpm dev
```
