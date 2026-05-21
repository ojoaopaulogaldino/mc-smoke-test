# JSAAI — Frontend Bootstrap

Projeto React com Next.js 15 exibindo a página inicial com a mensagem "funcionou".

## Pré-requisitos

- Node.js 20 LTS (recomendado: usar [nvm](https://github.com/nvm-sh/nvm))
- pnpm

```bash
nvm use
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
│       ├── layout.tsx    # Root layout
│       └── page.tsx      # Página inicial
├── public/               # Assets estáticos
├── .nvmrc                # Versão do Node (20 LTS)
├── next.config.ts        # Configuração do Next.js
├── package.json          # Dependências e scripts
├── tsconfig.json         # Configuração TypeScript
└── README.md             # Este arquivo
```

## Observações

- Para usar outra porta: `PORT=3001 pnpm dev`
