from typing import List, Dict, Any

# Importa as PORTAS (abstrações) do domínio
from domain.ports.table_repository import TableRepositoryPort
from domain.ports.product_repository import ProductRepositoryPort
from domain.ports.order_repository import OrderRepositoryPort # (NOVO) Importa a porta do pedido

# Importa os Modelos e Exceções
from domain.models import Order, Product, Table
from domain.exceptions import (
    TableNotFoundException, 
    ProductNotFoundException, 
    BusinessRuleException
)


class CreateOrderUseCase:
    """
    Caso de uso para criar um novo pedido e associá-lo a uma mesa.
    """
    
    def __init__(
        self, 
        table_repository: TableRepositoryPort,
        product_repository: ProductRepositoryPort,
        order_repository: OrderRepositoryPort  # (NOVO) Adiciona o repositório de pedidos
    ):
        """
        O construtor recebe todos os repositórios necessários.
        """
        self.table_repository = table_repository
        self.product_repository = product_repository
        self.order_repository = order_repository # (NOVO) Salva o repositório

    def execute(self, table_id: int, items_data: List[Dict[str, Any]]) -> Order:
        """
        Executa a lógica de criação do pedido.
        
        Args:
            table_id: O ID da mesa que está fazendo o pedido.
            items_data: Uma lista de dicionários, cada um contendo:
                        {"product_id": int, "quantity": int}
            
        Returns:
            O objeto Order recém-criado (já com seu ID do banco).
            
        Raises:
            TableNotFoundException: Se a mesa não for encontrada.
            ProductNotFoundException: Se algum produto da lista não for encontrado.
            BusinessRuleException: Se a lógica de domínio falhar
                                   (ex: mesa não está ocupada, 0 produtos).
        """
        
        # 1. Buscar o Agregado Raiz (a Mesa)
        table = self.table_repository.find_by_id(table_id)
        if not table:
            raise TableNotFoundException(f"Mesa {table_id} não encontrada.")

        # 2. Criar a nova entidade Order em memória
        new_order = Order(id=0, table_number=table_id)
        
        if not items_data:
            raise BusinessRuleException("Não é possível criar um pedido vazio.")

        try:
            # 3. Buscar produtos e popular o pedido (usando lógica de domínio)
            for item in items_data:
                product_id = item.get("product_id")
                quantity = item.get("quantity")
                
                product = self.product_repository.find_by_id(product_id)
                if not product:
                    raise ProductNotFoundException(f"Produto {product_id} não encontrado.")
                
                # Chama a lógica de domínio para adicionar o item
                new_order.add_item(product, quantity)

            # 4. Adicionar o novo pedido ao Agregado Raiz (Mesa) em MEMÓRIA
            # A mesa validará se pode aceitar um novo pedido
            table.add_new_order(new_order)

        except (ValueError, ProductNotFoundException) as e:
            # Captura erros de lógica (ex: "pedido já concluído")
            # ou o ProductNotFoundException
            raise BusinessRuleException(str(e))
            
        # 5. Persistir o Agregado Raiz (Mesa)
        # (ALTERADO): Isto salva APENAS o estado da mesa (ex: se o status mudasse)
        # Na prática, a mesa não muda neste caso de uso, 
        # mas manter isso não é prejudicial.
        self.table_repository.save(table)
        
        # 6. Persistir o NOVO Agregado (Pedido)
        # (NOVO): Chamamos explicitamente o repositório de pedidos
        # para salvar o novo pedido e seus itens.
        # O new_order (que tinha id=0) é salvo e recebe seu ID real.
        saved_order = self.order_repository.save(new_order)
        
        # 7. Retornar o novo pedido
        return saved_order # (ALTERADO) Retorna o objeto com o ID atualizado