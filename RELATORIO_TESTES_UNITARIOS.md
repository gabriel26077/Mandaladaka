# 🧪 Testes da Camada de Domínio (Mandaladaka)

## 📌 Visão Geral

A primeira bateria de testes da camada de domínio foi concluída com foco
total na entidade **Order**.\
Mesmo que apenas essa entidade tenha sido testada diretamente, outros
módulos do domínio acabaram recebendo cobertura indireta durante a
execução.



###  📌 O teste pode ser encontrado dentro de backend/tests/domain/models/test_order.py 📌 

## 🎯 Objetivo dos Testes

-   Validar corretamente o comportamento interno das entidades
-   Garantir a integridade das regras de negócio
-   Testar casos de uso embutidos na entidade Order
-   Manter isolamento total da infraestrutura (sem banco, API, Flask)

## 🔍 Escopo Atual dos Testes

Nesta etapa, o foco foi exclusivo na entidade `Order`, cobrindo:

-   Mudança de status e transições válidas
-   Adição e remoção de itens
-   Cálculo de preço total
-   Impedimento de operações inválidas
-   Verificação das exceções esperadas

Mesmo sem testar diretamente outras entidades e use cases, algumas delas
receberam cobertura mínima por serem carregadas ou referenciadas durante
a execução.

## ▶️ Comando Utilizado para Executar os Testes

``` bash
pytest --cov=src --cov-report term-missing --cov-report html
```

## 📊 Resultado da Execução

### ✔️ Testes

    17 passed in 0.32s

### ✔️ Cobertura Específica do Domínio

A classe **Order** alcançou **100% de cobertura**, conforme planejado.\
Alguns outros módulos do domínio apresentaram cobertura parcial
incidental.

### 🖼️ Relatório Gerado

![Imagem com relatório dos testes unitários. Informação principal: A
classe order tem 100% de cobertura](print_testes.png)

## 🚀 Conclusão

Este primeiro passo estabelece uma base sólida para a camada de domínio:

-   A entidade **Order** está completamente validada
-   O domínio começa a ganhar confiabilidade estrutural
-   Podemos evoluir para testes das outras entidades e dos *use cases*
-   A arquitetura permanece limpa e isolada

Próximos passos incluem ampliar os testes para `Product`, `Table`,
`ItemOrder` e posteriormente os *use cases*, buscando aumentar a
cobertura geral atualmente em 12%.
