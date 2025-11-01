from abc import ABC, abstractmethod
from typing import List, Optional
from ..models import Order, OrderStatus

class OrderRepositoryPort(ABC):
    """
    Define a "Porta" (Interface) para o repositório de pedidos.
    """

    @abstractmethod
    def find_by_id(self, order_id: int) -> Optional[Order]:
        """Encontra um pedido pelo seu ID."""
        pass
    
    @abstractmethod
    def find_by_status(self, status: OrderStatus) -> List[Order]:
        """Encontra todos os pedidos com um status específico (para a cozinha)."""
        pass

    @abstractmethod
    def save(self, order: Order) -> Order:
        """
        Salva um pedido (novo ou existente).
        A implementação deve ser inteligente para salvar os ItemOrders associados.
        """
        pass