# JSAAI — Frontend Bootstrap

Página inicial React com Next.js 15 exibindo a mensagem "funcionou".

## Pré-requisitos

- [Node.js 20 LTS](https://nodejs.org/) (recomendado via [nvm](https://github.com/nvm-sh/nvm))
- [pnpm](https://pnpm.io/) (`npm install -g pnpm`)

Se usar nvm:

```bash
nvm install
nvm use
```

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

Para usar outra porta:

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
│       ├── globals.css   # Estilos globais (reset + centralização)
│       ├── layout.tsx    # Layout raiz
│       └── page.tsx      # Página inicial — exibe "funcionou"
├── public/               # Assets estáticos
├── .gitignore
├── .nvmrc
├── next.config.ts
├── package.json
├── README.md
└── tsconfig.json
```
