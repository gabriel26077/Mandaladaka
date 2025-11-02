# Mandaladaka - Backend

Este diretório contém o código-fonte da API de backend do sistema Mandaladaka, construída em Flask.

## Arquitetura: Hexagonal (Portas e Adaptadores)

Este projeto utiliza a **Arquitetura Hexagonal** (também conhecida como "Portas e Adaptadores"). O objetivo principal é isolar o "núcleo" da aplicação (a lógica de negócio) do "mundo exterior" (frameworks, bancos de dados, APIs, etc.).

* **O Núcleo (Domain):** Contém a lógica de negócio pura (Modelos e Casos de Uso). Ele não sabe nada sobre Flask ou MySQL.
* **As Portas (Ports):** São interfaces definidas *pelo Núcleo*. Elas são como "tomadas" que o núcleo expõe, dizendo: "Eu preciso de algo que faça *isso*".
* **Os Adaptadores (Adapters):** São as implementações concretas que se "conectam" às Portas. Eles são o "mundo exterior" (Flask, MySQL) que implementam as regras definidas pelo núcleo.

**Analogia:** Pense no **Núcleo** como um computador. Ele tem portas USB (`ports.py`). O computador não se importa se você vai plugar um mouse, um teclado ou um pendrive (os `adapters`), desde que eles "falem a língua" da porta USB.

## Estrutura de Pastas

A arquitetura se reflete diretamente na organização das pastas dentro de `src/`.

```
backend/
├── requirements.txt   # Dependências do Python
├── run.py             # Ponto de entrada para iniciar o servidor
├── venv/              # Ambiente virtual do Python
└── src/               # Pacote principal do código-fonte
    ├── __init__.py    # "Fábrica" da aplicação (create_app), onde a MÁGICA acontece
    │
    ├── domain/        # <-- O NÚCLEO (Sem Flask/SQL)
    │   ├── models.py      # Nossos objetos de negócio (ex: dataclass Product)
    │   ├── ports.py       # As "Portas": interfaces que o núcleo precisa
    │   └── use_cases/     # A lógica de negócio (ex: GetVisibleProductsUseCase)
    │
    └── adapters/      # <-- O MUNDO EXTERIOR (Com Flask/SQL)
        ├── web/           # Adaptador de "Entrada" (Driving Adapter)
        │   └── routes.py  # Converte requisições HTTP em chamadas de Casos de Uso
        │
        └── db/            # Adaptador de "Saída" (Driven Adapter)
            ├── db_config.py # Configurações de conexão do banco
            └── mysql_repository.py # Implementação CONCRETA da porta de repositório
```

## Conceitos-Chave

### `src/domain` (O Núcleo)
O coração da aplicação. Totalmente independente de frameworks.
* `models.py`: Define as estruturas de dados puras (ex: `Product`).
* `use_cases/`: Contém as classes que orquestram a lógica de negócio (ex: `GetVisibleProductsUseCase`). Eles são chamados pelos adaptadores de entrada (como `routes.py`).

### `src/domain/ports.py` (As Portas)
Este arquivo é crucial. Ele define os **contratos** (interfaces abstratas) que o núcleo espera que o mundo exterior implemente.

* **Exemplo:** `AbstractProductRepository`
* **Propósito:** O `GetVisibleProductsUseCase` não sabe o que é MySQL. Ele apenas diz: "Eu preciso de um `repository` que tenha um método `get_visible_products()`", como definido na porta `AbstractProductRepository`. Isso permite que a lógica de negócio seja testada em isolamento, usando um repositório falso em memória.

### `src/adapters` (Os Adaptadores)
Esta pasta contém o "código-cola" que conecta o **Núcleo** ao mundo real. Eles dependem do Domínio, mas o Domínio não depende deles.

Existem dois tipos de adaptadores:

#### 1. `src/adapters/web/` (Adaptador de Entrada / "Driving")
Este adaptador **inicia** a ação na aplicação.
* `routes.py`: É um adaptador HTTP (Flask). Sua única responsabilidade é:
    1.  Receber uma requisição HTTP (ex: `GET /api/products`).
    2.  Chamar o Caso de Uso correspondente (ex: `get_products_use_case.execute()`).
    3.  Converter a resposta do Caso de Uso (que é um objeto `Product`) em JSON e devolvê-la.
    * **Não contém lógica de negócio ou SQL.**

#### 2. `src/adapters/db/` (Adaptador de Saída / "Driven")
Este adaptador é **chamado** pela aplicação (através de uma porta) para executar uma ação no mundo exterior.
* `mysql_repository.py`: É um adaptador de persistência. Ele **implementa** a interface `AbstractProductRepository` definida em `ports.py`.
    * **Propósito:** É aqui que o SQL "vive". Esta classe sabe como se conectar ao MySQL, executar a query `SELECT * FROM products` e converter o resultado do banco em objetos `Product` que o Domínio entende.
* `db_config.py`: Apenas armazena os detalhes de conexão (host, usuário, senha) para manter o `mysql_repository.py` limpo.

### `src/__init__.py` (O "Montador")
Este arquivo é o ponto de encontro. A função `create_app()` é responsável por:
1.  Criar a instância do Adaptador de Saída (ex: `MySQLProductRepository`).
2.  Criar a instância do Caso de Uso, "injetando" o adaptador nele (ex: `GetVisibleProductsUseCase(repository=...)`).
3.  Criar o Adaptador de Entrada (o `main_blueprint`), "injetando" o caso de uso nele.
4.  Retornar a aplicação Flask pronta.

## Como Executar

1.  **Ative o ambiente virtual:**
    ```bash
    source venv/bin/activate
    # ou "venv\Scripts\activate" no Windows
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a aplicação:**
    ```bash
    python run.py
    ```
    O servidor estará rodando em `http://localhost:5000`.