from typing import List

# Importa a PORTA (abstração) do domínio
from domain.ports.order_repository import OrderRepositoryPort

# Importa os Modelos (incluindo o Enum de status)
from domain.models import Order, OrderStatus


class ListPendingOrdersUseCase:
    """
    Caso de uso para listar todos os pedidos que estão
    com status 'PENDING' (pendentes), para a tela da cozinha.
    """
    
    def __init__(self, order_repository: OrderRepositoryPort):
        """
        O construtor recebe o repositório de pedidos.
        """
        self.order_repository = order_repository

    def execute(self) -> List[Order]:
        """
        Executa a busca por todos os pedidos pendentes.
        
        A autenticação (verificar se o usuário é da cozinha ou admin)
        é tratada pela camada de API.
        
        Returns:
            Uma lista de objetos Order que estão com status 'PENDING'.
        """
        
        # 1. Chamar a porta do repositório
        pending_orders = self.order_repository.find_by_status(
            OrderStatus.PENDING
        )
        
        # 2. Retornar a lista
        return pending_orders