# Modelagem e Diagramas do Projeto Mandaladaka

Este documento descreve os diagramas UML criados para modelar a arquitetura e o comportamento do sistema de gerenciamento de restaurante Mandaladaka, justificando a escolha de cada um.

Os arquivos de imagem dos diagramas estão localizados no diretório `/Diagrams`.

## 1. Diagrama Estrutural

### Diagrama de Classes

**Descrição:**
O Diagrama de Classes fornece uma visão estática da estrutura do sistema. Ele detalha as principais classes (`User`, `Waiter`, `Order`, `Product`, etc.), seus atributos, métodos e, fundamentalmente, os relacionamentos entre elas (como herança, associação e composição).

**Justificativa:**
Este diagrama foi escolhido por ser a base da modelagem orientada a objetos. Ele é essencial para que a equipe de desenvolvimento compreenda a estrutura do código, as responsabilidades de cada classe e como as entidades de negócio se conectam. Serve como um guia para a implementação das classes e do esquema do banco de dados, garantindo consistência e uma arquitetura bem definida.

## 2. Diagramas Comportamentais

### Diagrama de Casos de Uso

**Descrição:**
O Diagrama de Casos de Uso oferece uma visão de alto nível das funcionalidades do sistema a partir da perspectiva do usuário. Ele identifica os atores (`Waiter`, `Admin`) e as principais interações (casos de uso) que eles podem realizar no sistema, como "Realizar Novo Pedido" ou "Gerenciar Produtos".

**Justificativa:**
Este diagrama foi criado para definir e comunicar de forma clara o escopo funcional do projeto. Ele é uma excelente ferramenta para garantir que todos os envolvidos (desenvolvedores, stakeholders) tenham um entendimento comum sobre *o que* o sistema deve fazer, servindo como base para o desenvolvimento e os testes das funcionalidades.
