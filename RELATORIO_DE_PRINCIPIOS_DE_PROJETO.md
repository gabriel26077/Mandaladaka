## Resumo dos princípios
### Responsabilidade única
Consiste em separar comportamentos diferentes em partes diferentes do código, assim, podemos reutilizar um comportamento sem precisar executar os demais. Assim cada componente tem um único comportamento coeso.
### Segregação de responsabilidades
Estende o princípio anterior para considerar que interfaces devem ser mínimas e coesas. Então se uma responsabilidade cabe apenas para uma parte das aplicações da interface, essa responsabilidade deve ser especificada em uma extensão dessa interface, não na interface global.
### Inversão de dependências
Ou "Prefira Interfaces a Classes". Abstrações são mais estáveis que implementações concretas. Assim, é preferível que seu código (e.g., uma classe ou argumento de função) dependa de uma interface ou classe abstrata (e.g., `List`) do que de uma implementação concreta (e.g., `DoubleLinkedList`). Para implementar isso é interessante pensar em injetar essas dependências como argumento. Ou seja, o cliente já injeta a dependência concreta que prefere usar.
### Preferir Composição a Herança
Herança: `class A extends B` é o mesmo que `A` é um tipo de `B`.
Composição: `class A{B b;}`, quando `A` possui uma instância de `B`. Assim, ao invés de `A` extender os comportamentos de `B`, ele usa uma instância para faze-los.
Usando composição, podemos não acessar/alterar o comportamento de `B` desnecessariamente.
### Demeter
Evite longas cadeias de chamadas de métodos, em que uma instância acessa o atributo do atributo do atributo do atributo... Isto viola o encapsulamento de seus atributos.

A implementação de um método deve invocar apenas os seguintes outros métodos:
- de sua própria classe (caso 1)
- de objetos passados como parâmetros (caso 2)
- de objetos criados pelo próprio método (caso 3)
- de atributos da classe do método (caso 4)

> Pessoalmente acho um princípio pouco relevante, e com muitas exceções. Por exemplo:

Em vários casos uma interface pode querer definir uma série de operações que modificam uma instância criando uma cópia (e.g.: `Array.filter(x): Array`), de modo que cabe fazer essa série de alterações sem criar uma variável específica, fazendo uma cadeia (e.g.: `.filter(x).filter(y).filter(z)`).
### Aberto/fechado
Uma classe deve estar fechada para modificações, mas aberta para extensões. Assim, é possível modificar uma classe sem precisar modificar sua implementação, mas sim extender ou sobrecarregar sua funcionalidade. Para isso existem diversos padrões de projeto possíveis.
### Substituição de Liskov
Este princípio basicamente diz que uma classe `S` só é de fato uma subclasse de `T` quando o comportamento implementado por `S` que sobrescreve os comportamentos de `T` é o mesmo.
## Aplicação no projeto
Nosso projeto já respeita os princípios de Responsabilidade única e  segregação de responsabilidades. Temos classes que apenas representam modelos de entidades e que não apresentam métodos e classes que representam apenas comportamentos particulares, para cada usecase. Assim, cada classe possui um papel único e claro e cada método desempenha apenas uma função particular.

O projeto não possui muitos casos em que se haja extensão de comportamento para haver discussões como os princípios de Preferir composição a herança, Aberto/fechado e Substituição de Liskov. O caso das classes que estendem `User` em fato segue o princípio de Liskov (pois nenhuma das classes sequer possui comportamento para ser substituído).

Quanto ao princípio de Demeter, precisamos tomar cuidado durante o desenvolvimento para não violá-lo.

# Revisão

## 🧩 Padrões de Projeto Utilizados

A arquitetura do Mandaladaka segue princípios modernos de engenharia de software, utilizando padrões de projeto que garantem organização, isolamento, testabilidade e evolução do sistema.

### 🔶 Arquitetura Hexagonal (Ports & Adapters)
O sistema separa claramente o núcleo de domínio das interfaces externas.

- **Portas (Ports):** interfaces que o domínio expõe.
- **Adaptadores (Adapters):** implementações concretas que se conectam ao banco de dados e ao Flask.

### 🔷 Domain-Driven Design (DDD – Camada de Domínio)
A camada `src/domain/` segue conceitos táticos de DDD:
- Entidades
- Agregados
- Exceções de domínio
- Casos de uso (Application Services)

### 🔧 Repository Pattern
Repositórios são definidos como portas:
```python
class OrderRepositoryPort(ABC):
```
E implementados por adaptadores.

### 🎛 Dependency Injection
Use cases recebem dependências via construtor.

### 📤 Command Pattern
Use cases seguem o formato:
```python
def execute(...)
```

### 📌 Documentação Complementar
Para detalhes sobre testes da camada de domínio, consulte:

👉 **TESTS_DOMAIN.md**