# Frontend - Sistema de Gestão MDK

Este diretório contém todo o código-fonte do frontend para o projeto MDK, um Sistema de gestão de pedidos para restaurantes.

O objetivo é criar uma interface moderna, rápida e intuitiva para facilitar a operação diária, desde a seleção de mesas até o fechamento da conta.

## ✨ Funcionalidades Principais

* **Gestão de Mesas:** Visualização gráfica do layout das mesas, com status de livre/ocupado.
* **Seleção de Clientes:** Atribuição de uma quantidade de clientes a uma mesa.
* **Criação de Pedidos:** Interface para adicionar produtos a um pedido associado a uma mesa.
* **Navegação Intuitiva:** Um menu lateral para acesso rápido às principais seções do sistema (Cardápio, Pagamentos, etc.).

## 🚀 Tecnologias Utilizadas

Este projeto foi construído utilizando o ecossistema React com as seguintes tecnologias:

* **[Next.js](https://nextjs.org/):** Framework React para produção, que oferece renderização no servidor, geração de sites estáticos e uma ótima experiência de desenvolvimento.
* **[React](https://react.dev/):** Biblioteca para construir interfaces de usuário.
* **[TypeScript](https://www.typescriptlang.org/):** Superset do JavaScript que adiciona tipagem estática ao código, aumentando a robustez e facilitando a manutenção.

## 📂 Estrutura de Pastas

O projeto utiliza a estrutura do **App Router** do Next.js, que é organizada por rotas.

```
frontend/
├── src/
│   └── app/
│       ├── globals.css     # Estilos globais da aplicação.
│       ├── layout.tsx      # Layout principal que envolve todas as páginas.
│       └── page.tsx        # A página principal (Home, a tela de mesas).
│
├── public/                 # Arquivos estáticos (imagens, ícones, fontes).
│
├── next.config.js          # Arquivo de configuração do Next.js.
└── package.json            # Dependências e scripts do projeto.
```

* **`src/app/`**: É o coração do projeto. Cada pasta dentro de `app` representa uma rota (uma URL) na aplicação. O arquivo `page.tsx` é a interface daquela rota.
* **`public/`**: Contém todos os arquivos que serão servidos publicamente, como os ícones das mesas e da navegação.

## ⚙️ Como Rodar o Projeto

Siga os passos abaixo para executar o projeto em seu ambiente de desenvolvimento.

1.  **Pré-requisitos:**
    * [Node.js](https://nodejs.org/en) (versão 18 ou superior).
    * `npm` ou `yarn`.

2.  **Navegue até a pasta do frontend:**
    ```bash
    cd frontend
    ```

3.  **Instale as dependências do projeto:**
    ```bash
    npm install
    ```

4.  **Inicie o servidor de desenvolvimento:**
    ```bash
    npm run dev
    ```

5.  **Acesse a aplicação:**
    * Abra seu navegador e acesse [http://localhost:3000](http://localhost:3000).
