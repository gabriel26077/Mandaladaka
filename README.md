# Eng-de-Software-UFRN

Repositório de exemplo para as atividades da disciplina de Engenharia de Software da UFRN.

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Modelagem e Diagramas UML](#modelagem-e-diagramas-uml)
- [Componentes](#componentes)
- [Como clonar ou baixar](#como-clonar-ou-baixar)
- [Como Executar](#como-executar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Licença](#licença)

## Sobre o Projeto

### Título
Mandaladaka

### Descrição
Um AppWeb de gerenciamento de restaurante para auxiliar na organização de mesas, pedidos e ítens disponíveis no estoque/cardápio.

## Modelagem e Diagramas UML

A arquitetura e o comportamento do sistema foram modelados utilizando diagramas UML para garantir clareza e consistência no desenvolvimento.

- **Diagrama de Classes:** Detalha a estrutura estática, as classes e seus relacionamentos.
- **Diagrama de Casos de Uso:** Mostra as funcionalidades do sistema pela perspectiva dos usuários (Atores).

Os diagramas visuais estão localizados na pasta `Diagrams` e a documentação detalhada sobre eles pode ser encontrada no arquivo `Diagramas.md`.

### Componentes
- Gabriel Sebastião do Nascimento Neto
- Sara Gabrielly do Nascimento Silva
- Icaro Bruno Silbe Cortês

## Como clonar ou baixar

Você pode obter este repositório de três formas:

### Clonar via HTTPS

```bash
git clone https://github.com/gabriel26077/Mandaladaka
```

Isso criará uma cópia local do repositório em sua máquina.

### Clonar via SSH

Se você já configurou sua chave SSH no GitHub, pode clonar usando:

```bash
git clone git@github.com:gabriel26077/Mandaladaka.git
```

Isso criará uma cópia local do repositório em sua máquina.

### Baixar como ZIP

1. Acesse a página do repositório no GitHub:
   [https://github.com/gabriel26077/Mandaladaka](https://github.com/gabriel26077/Mandaladaka)
2. Clique no botão **Code** (verde).
3. Selecione **Download ZIP**.
4. Extraia o arquivo ZIP para o local desejado em seu computador.

## Como Executar

Este projeto utiliza `make` para automatizar o processo de instalação e execução.

**Pré-requisito:** Você precisa ter o `make` instalado em seu sistema.

Siga os passos abaixo:

1.  **Configurar o ambiente:**
    Primeiro, copie o arquivo de exemplo `config.mk.example` para um novo arquivo chamado `config.mk`.

    ```bash
    cp config.mk.example config.mk
    ```

    Em seguida, edite o `config.mk` com suas configurações locais (senhas de banco, chaves de API, etc.).

2.  **Instalar dependências:**
    Execute o comando abaixo para instalar todas as dependências do backend (Flask) e do frontend (Next.js).

    ```bash
    make install-all
    ```

3.  **Inicializar o Banco de Dados:**
    (Opcional, execute na primeira vez ou se precisar resetar o banco)
    Este comando irá criar as tabelas e popular o banco de dados.

    ```bash
    make init-db
    ```

4.  **Rodar os serviços:**
    Você precisará de dois terminais abertos.

    - No **primeiro terminal**, inicie o backend:
      ```bash
      make run-back
      ```

    - No **segundo terminal**, inicie o frontend:
      ```bash
      make run-front
      ```

Para encerrar os serviços, pressione `Ctrl+C` em cada um dos terminais.

## Estrutura do Projeto

```
Mandaladaka/
├── Makefile                 # Arquivo de automação 'make' para build, run e install.
├── config.mk                # Arquivo de configuração local (ignorado pelo git).
├── config.mk.example        # Exemplo de arquivo de configuração.
├── LICENSE                  # Licença MIT do projeto.
├── README.md                # Este arquivo de documentação.
├── backend/                 # Contém o código-fonte do backend (Flask).
├── frontend/                # Contém o código-fonte do frontend (Next.js).
├── database/                # Contém os scripts SQL para criação e população do banco.
├── Diagrams/                # Contém os arquivos de imagem dos diagramas UML.
├── Diagramas.md             # Documentação detalhada dos diagramas UML.
├── backlog_user_stories.md  # Documento com o backlog e histórias de usuário.
└── 'Relatório de Princípios de projeto.md' # Documentação de arquitetura e design.
```

## Licença

Este projeto está licenciado sob a **Licença MIT**. Veja o arquivo `LICENSE` para mais detalhes.