# Importa a PORTA (abstração) do domínio
from domain.ports.order_repository import OrderRepositoryPort

# Importa o Modelo e as Exceções
from domain.models import Order
from domain.exceptions import OrderNotFoundException, BusinessRuleException


class StartOrderPreparationUseCase:
    """
    Caso de uso para a cozinha marcar um pedido como
    'IN_PROGRESS' (em preparo).
    """
    
    def __init__(self, order_repository: OrderRepositoryPort):
        """
        O construtor recebe o repositório de pedidos.
        """
        self.order_repository = order_repository

    def execute(self, order_id: int) -> Order:
        """
        Executa a lógica de negócio para iniciar o preparo de um pedido.
        
        Args:
            order_id: O ID do pedido que a cozinha começou a preparar.
            
        Returns:
            O objeto Order atualizado (agora com status 'IN_PROGRESS').
            
        Raises:
            OrderNotFoundException: Se o pedido com o ID fornecido não existir.
            BusinessRuleException: Se a lógica de domínio falhar
                                   (ex: pedido não estava 'PENDING').
        """
        
        # 1. Buscar o Agregado Raiz (o Pedido)
        order = self.order_repository.find_by_id(order_id)
        
        # 2. Validar se a entidade existe
        if not order:
            raise OrderNotFoundException(f"Pedido {order_id} não encontrado.")
            
        # 3. Chamar a lógica de negócio (que está no Domínio)
        try:
            # O caso de uso "comanda" o modelo de domínio
            order.mark_as_in_progress()
            
        except ValueError as e:
            # Captura exceções de regras de negócio (ex: "Pedido não está pendente")
            raise BusinessRuleException(str(e))
            
        # 4. Persistir a mudança de estado
        updated_order = self.order_repository.save(order)
        
        # 5. Retornar a entidade atualizada
        return updated_order