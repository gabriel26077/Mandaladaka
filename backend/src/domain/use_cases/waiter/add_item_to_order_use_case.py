# Importa as PORTAS (abstrações) do domínio
from domain.ports.order_repository import OrderRepositoryPort
from domain.ports.product_repository import ProductRepositoryPort

# Importa os Modelos e Exceções
from domain.models import Order, Product
from domain.exceptions import (
    OrderNotFoundException, 
    ProductNotFoundException, 
    BusinessRuleException
)


class AddItemToOrderUseCase:
    """
    Caso de uso para adicionar um ou mais itens a um pedido
    que já existe (ex: "O cliente pediu mais uma coca").
    """
    
    def __init__(
        self, 
        order_repository: OrderRepositoryPort,
        product_repository: ProductRepositoryPort
    ):
        """
        O construtor recebe os repositórios necessários.
        """
        self.order_repository = order_repository
        self.product_repository = product_repository

    def execute(self, order_id: int, product_id: int, quantity: int) -> Order:
        """
        Executa a lógica de adicionar o item ao pedido.
        
        Args:
            order_id: O ID do pedido a ser modificado.
            product_id: O ID do produto a ser adicionado.
            quantity: A quantidade de produtos a adicionar.
            
        Returns:
            O objeto Order atualizado.
            
        Raises:
            OrderNotFoundException: Se o pedido não for encontrado.
            ProductNotFoundException: Se o produto não for encontrado.
            BusinessRuleException: Se a lógica de domínio falhar
                                   (ex: pedido já concluído, 0 produtos).
        """
        
        # 1. Buscar o Agregado Raiz (o Pedido)
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise OrderNotFoundException(f"Pedido {order_id} não encontrado.")

        # 2. Buscar a entidade Produto
        product = self.product_repository.find_by_id(product_id)
        if not product:
            raise ProductNotFoundException(f"Produto {product_id} não encontrado.")

        # 3. Chamar a lógica de negócio (que está no Domínio)
        try:
            # O caso de uso "comanda" o modelo de domínio
            order.add_item(product, quantity)
            
        except ValueError as e:
            # Captura exceções de regras de negócio (ex: "Pedido já concluído")
            raise BusinessRuleException(str(e))
            
        # 4. Persistir a mudança de estado
        # O repositório salva o objeto 'order' que agora está "sujo"
        # (com um novo ItemOrder ou um ItemOrder existente atualizado)
        updated_order = self.order_repository.save(order)
        
        # 5. Retornar a entidade atualizada
        return updated_order