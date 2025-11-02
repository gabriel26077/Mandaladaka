# Importa a PORTA (abstração) do domínio
from domain.ports.order_repository import OrderRepositoryPort

# Importa o Modelo e as Exceções
from domain.models import Order
from domain.exceptions import OrderNotFoundException, BusinessRuleException


class CompleteOrderPreparationUseCase:
    """
    Caso de uso para a cozinha marcar um pedido como
    'COMPLETED' (preparo concluído e pronto para entrega).
    """
    
    def __init__(self, order_repository: OrderRepositoryPort):
        """
        O construtor recebe o repositório de pedidos.
        """
        self.order_repository = order_repository

    def execute(self, order_id: int) -> Order:
        """
        Executa a lógica de negócio para concluir o preparo de um pedido.
        
        Args:
            order_id: O ID do pedido que a cozinha finalizou.
            
        Returns:
            O objeto Order atualizado (agora com status 'COMPLETED').
            
        Raises:
            OrderNotFoundException: Se o pedido com o ID fornecido não existir.
            BusinessRuleException: Se a lógica de domínio falhar
                                   (ex: pedido não estava 'IN_PROGRESS').
        """
        
        # 1. Buscar o Agregado Raiz (o Pedido)
        order = self.order_repository.find_by_id(order_id)
        
        # 2. Validar se a entidade existe
        if not order:
            raise OrderNotFoundException(f"Pedido {order_id} não encontrado.")
            
        # 3. Chamar a lógica de negócio (que está no Domínio)
        try:
            # O caso de uso "comanda" o modelo de domínio
            order.mark_as_completed()
            
        except ValueError as e:
            # Captura exceções de regras de negócio (ex: "Pedido não está em preparo")
            raise BusinessRuleException(str(e))
            
        # 4. Persistir a mudança de estado
        updated_order = self.order_repository.save(order)
        
        # 5. Retornar a entidade atualizada
        return updated_order