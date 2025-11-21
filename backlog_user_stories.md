
# Backlog - Sistema de Gerenciamento de Restaurante

## User Story 1 – Gerenciar Mesa
**Descrição:**  
Como **garçom**, gostaria de **adicionar e remover mesas**, para organizar os atendimentos.  

**Prioridade:** Alta  
**Estimativa:** 8 pontos  

**Critérios de Aceitação:**  
1. O usuário deve estar autenticado.  
2. O usuário deve ser capaz de visualizar mesas já criadas.  
3. O usuário deve ser capaz de criar novas mesas.  
4. O usuário deve ser capaz de deletar mesas existentes.  
5. O usuário deve ser capaz de fechar uma comanda.  

---

## User Story 2 – Gerenciar Pedido
**Descrição:**  
Como **garçom**, gostaria de visualizar os pedidos pendentes em tempo real e marcar o início do preparo, para agilizar a entrega dos pratos.

**Estimativa:** 5 pontos  

**Critérios de Aceitação:**  
1. O usuário deve estar autenticado.  
2. O usuário deve ser capaz de vincular um pedido a uma mesa.  
3. O usuário deve ser capaz de excluir um pedido.  
4. O usuário deve ser capaz de marcar um pedido como concluído.  

---

## User Story 3 – Gerenciar Fila de Preparos
**Descrição:**  
Como **cozinheiro**, gostaria de **adicionar, visualizar, editar e remover itens do cardápio**, para manter as opções atualizadas.  

**Prioridade:** Alta  
**Estimativa:** 5 pontos  

**Critérios de Aceitação:**  
1. O usuário deve ser capaz de visualizar uma lista de pedidos com status "Pendente".
2. O sistema deve exibir os itens e quantidades de cada pedido de forma clara (Cards).
3. O usuário deve ser capaz de alterar o status do pedido para "Em Preparo" (Botão Iniciar Preparo).
4. O pedido deve desaparecer da lista de pendentes após o início do preparo.

## User Story 4 - Processar Fechamento de Caixa
**Descrição**
Como **caixa**, gostaria de visualizar o consumo total da mesa e processar o pagamento, para liberar a mesa para novos clientes.

**Prioridade:** Alta  
**Estimativa:** 5 pontos  

**Critérios de Aceitação:**  
1. O usuário deve visualizar o resumo de todos os itens consumidos na mesa.
2. O sistema deve calcular automaticamente o subtotal e a taxa de serviço (10%).
3. O usuário deve poder confirmar o pagamento.
4. Ao confirmar o pagamento, o sistema deve alterar o status da mesa para "Livre" (Available).

