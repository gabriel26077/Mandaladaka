# Mandaladaka - Frontend

Este diretório contém o código-fonte do cliente (Web App) do sistema Mandaladaka, construído com **Next.js 13+** e **TypeScript**, utilizando o **App Router**.

## 🚀 Sobre o Projeto

O frontend é responsável por toda a interface com o usuário, consumindo a API do backend (Flask) para gerenciar mesas, pedidos e cardápio.

## 📁 Estrutura de Pastas (App Router)

O projeto segue a estrutura de pastas padrão do Next.js 13+, que é baseada em rotas e componentes.

```
frontend/
├── design_ui/             # Arquivos de design e protótipos (ex: Figma)
├── public/                # Assets estáticos (ícones, imagens)
│   ├── icons/
│   └── images/categories/
├── src/
│   ├── app/               # <-- O Coração do App Router
│   │   ├── login/
│   │   ├── menu/
│   │   ├── order/
│   │   ├── payment/
│   │   ├── settings/
│   │   │
│   │   ├── layout.tsx     # Layout principal (com Sidebar/Header)
│   │   ├── page.tsx       # Página principal (Home / Lista de Mesas)
│   │   └── globals.css
│   │
│   └── components/        # <-- Componentes Reutilizáveis
│       ├── header.tsx
│       └── sidebar.tsx
│
├── .gitignore
├── package.json
└── README.md              # Este arquivo
```

### Conceitos-Chave da Estrutura

* `src/app/`: O núcleo da aplicação. Cada pasta dentro de `app` se torna um segmento de rota na URL (ex: `src/app/menu` vira `http://.../menu`).
* `page.tsx`: Define a UI pública para uma rota. (Ex: `src/app/order/page.tsx` é a página da rota `/order`).
* `layout.tsx`: Define uma UI compartilhada (como a `Sidebar` e o `Header`) que envolve as `page.tsx` filhas.
* `*.module.css`: Usamos CSS Modules (ex: `order.module.css`) para estilização local e escopada por componente, evitando conflitos de classes.
* `src/components/`: Contém componentes React reutilizáveis (ex: `Sidebar`) que não são rotas.

## 📊 Funcionalidades e Status Atual
> **🎨 Status da UI (Design)**
> A interface do usuário (UI) atual é funcional, mas ainda passará por um refinamento visual e de usabilidade. A página de **Pedidos & Comandas (`/order`)**, em particular, é a prioridade para futuras melhorias de design.

### ✅ Concluído e 100% Integrado

* **Login:** Página de autenticação que se comunica com a API.
* **Home (Lista de Mesas):**
    * Busca e exibe todas as mesas.
    * Mostra o status de cada mesa (livre, ocupada, número de pessoas).
* **Cardápio (Menu):**
    * Busca e exibe todos os produtos e suas categorias.
    * Permite a seleção de itens para um novo pedido.

### ⚠️ Em Desenvolvimento (Parcialmente Implementado)

* **Painel — Pedidos & Comandas (`/order`):**
    * **Aba "Pedidos Pendentes":** Funcional. Faz a requisição ao backend e exibe corretamente os pedidos pendentes na cozinha.
    * **Aba "Comandas":** Implementação inicial.
        * **❌ O que falta:** As comandas listadas não são clicáveis para consultar os pedidos de cada uma.
        * **❌ O que falta:** O botão "Fechar Comanda" não funciona (será alterado para "Ir para Pagamento").
        * **❌ O que falta:** O botão "Novo Pedido" redireciona para `/menu`, mas não passa o ID da mesa/comanda, impedindo que o pedido seja associado corretamente.

### 📋 Próximos Passos (To-Do)

1.  **Pagamento:** Implementar a página `/payment`, que conterá a lógica final para "Fechar Mesa".
2.  **Fluxo de Comandas:**
    * Tornar as comandas na aba "Comandas" clicáveis para consultar os pedidos de cada uma.
    * Corrigir o fluxo "Adicionar Pedido" (via comanda) para que o ID da mesa seja enviado corretamente para a página `/menu`.
3.  **Botões:** Alterar o botão "Fechar Comanda" para "Ir para Pagamento" e direcioná-lo para a nova página.

## 🛠️ Como Executar (Desenvolvimento)

Existem duas formas de rodar o frontend: usando o `make` (recomendado) ou manualmente com `npm`.

**Pré-requisito:** Você precisa ter o [Node.js](https://nodejs.org/) (v18 ou superior) instalado.

### 1. Usando `make` (Recomendado)

Este comando foi configurado no `Makefile` da raiz do projeto (`Mandaladaka/`) e cuida de tudo.

```bash
# No diretório raiz (Mandaladaka/), execute:
make run-front
```

### 2. Manualmente (NPM)

1.  **Navegue até a pasta:**
    ```bash
    cd frontend
    ```

2.  **Instale as dependências:**
    ```bash
    npm install
    ```

3.  **Variáveis de Ambiente:**
    Crie um arquivo `.env.local` na raiz da pasta `frontend/`. Ele é necessário para apontar para a API do backend.

    ```bash
    # frontend/.env.local
    NEXT_PUBLIC_API_URL=http://localhost:5000
    ```

4.  **Rode o servidor de desenvolvimento:**
    ```bash
    npm run dev
    ```

A aplicação estará disponível em `http://localhost:3000`.