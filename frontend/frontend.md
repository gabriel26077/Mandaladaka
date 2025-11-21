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
└── frontend.md              # Este arquivo
```

### Conceitos-Chave da Estrutura

* `src/app/`: O núcleo da aplicação. Cada pasta dentro de `app` se torna um segmento de rota na URL (ex: `src/app/menu` vira `http://.../menu`).
* `page.tsx`: Define a UI pública para uma rota. (Ex: `src/app/order/page.tsx` é a página da rota `/order`).
* `layout.tsx`: Define uma UI compartilhada (como a `Sidebar` e o `Header`) que envolve as `page.tsx` filhas.
* `*.module.css`: Usamos CSS Modules (ex: `order.module.css`) para estilização local e escopada por componente, evitando conflitos de classes.
* `src/components/`: Contém componentes React reutilizáveis (ex: `Sidebar`) que não são rotas.

## ✨ Funcionalidades Principais

### 1. 🗺️ Mapa de Mesas (Home)
- Visualização em tempo real do status das mesas.
- **Livre (Verde):** Permite abrir a mesa definindo o número de clientes.
- **Ocupada (Vermelha):** Permite acessar o menu ou fechar a conta.

### 2. 📝 Gestão de Pedidos & Cozinha (KDS)
- **Painel da Cozinha:** Lista pedidos pendentes vindos do banco de dados.
- **Fluxo de Preparo:** Botão "Iniciar Preparo" que comunica ao backend a mudança de status do pedido.
- **Design Otimizado:** Cards visuais com ícones para rápida leitura.

### 3. 💸 Pagamento & Fechamento
- Resumo detalhado de consumo.
- Cálculo automático de subtotal e taxa de serviço (10%).
- Simulação de pagamento (Dinheiro, Cartão, Pix).

### 4. 🎨 UI/UX Aprimorada
- **Sidebar Retrátil:** Menu lateral animado que maximiza o espaço de tela.
- **Design System:** Cores e componentes padronizados globalmente (`globals.css`).

---

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