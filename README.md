# JSAAI — Frontend Bootstrap

Projeto React inicializado com Next.js 15 + React 19 + TypeScript.

## Pré-requisitos

- **Node.js** 20 LTS (use [nvm](https://github.com/nvm-sh/nvm): `nvm use`)
- **pnpm** (instale com `npm install -g pnpm`)

## Instalação

Instale as dependências do projeto:

```bash
pnpm install
```

## Desenvolvimento

Inicie o servidor de desenvolvimento local:

```bash
pnpm dev
```

O servidor ficará disponível em [http://localhost:3000](http://localhost:3000).

Para usar outra porta:

```bash
PORT=3001 pnpm dev
```

## Build de produção

Gere o bundle de produção:

```bash
pnpm build
```

Para iniciar o servidor de produção após o build:

```bash
pnpm start
```

## Estrutura de pastas

```
.
├── src/
│   └── app/
│       ├── page.tsx       # Página inicial — exibe "funcionou"
│       ├── layout.tsx     # Layout raiz
│       └── globals.css    # Estilos globais (reset + centralização)
├── public/                # Arquivos estáticos
├── package.json           # Dependências e scripts
├── tsconfig.json          # Configuração TypeScript
├── next.config.ts         # Configuração Next.js
├── .nvmrc                 # Versão do Node.js (20 LTS)
└── README.md              # Este arquivo
```

## Tecnologias

- [Next.js 15](https://nextjs.org/) — framework React
- [React 19](https://react.dev/) — biblioteca de UI
- [TypeScript](https://www.typescriptlang.org/) — tipagem estática
- [pnpm](https://pnpm.io/) — gerenciador de pacotes
