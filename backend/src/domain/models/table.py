from dataclasses import dataclass, field
from typing import List
from enum import Enum
#from datetime import datetime

# Importa o modelo Order para a lista de pedidos
from .order import Order, OrderStatus

class TableStatus(str, Enum):
    """
    Define os status possíveis de uma Mesa.
    """
    AVAILABLE = 'available'  # Disponível (livre)
    OCCUPIED = 'occupied'    # Ocupada (com clientes, com ou sem pedidos)

@dataclass
class Table:
    """
    Representa uma Mesa no restaurante.
    É uma 'Raiz de Agregado' que gerencia uma lista de Pedidos (Orders)
    associados a ela durante uma sessão de cliente.
    """
    id: int  # O número da mesa (ex: 1, 2, 3...)
    status: TableStatus = TableStatus.AVAILABLE
    
    # NOVO: Quantidade de pessoas sentadas na mesa.
    # 0 (zero) quando a mesa está 'available'.
    number_of_people: int = 0
    
    # A lista de pedidos ATIVOS para esta mesa.
    orders: List[Order] = field(default_factory=list)

    # --- Propriedades (Lógica de Leitura) ---

    @property
    def total_bill(self) -> float:
        """
        Calcula a conta total da mesa, somando todos os pedidos
        que não foram cancelados.
        """
        return sum(
            order.total_price 
            for order in self.orders 
            if order.status != OrderStatus.CANCELLED
        )

    # --- Métodos de Comportamento (Lógica de Escrita) ---

    def open_table(self, number_of_people: int):
        """
        Abre a mesa para clientes, marcando-a como ocupada e 
        registrando o número de pessoas.
        """
        if self.status == TableStatus.OCCUPIED:
            raise ValueError(f"A Mesa {self.id} já está ocupada.")
            
        if number_of_people <= 0:
            raise ValueError("O número de pessoas deve ser maior que zero.")
        
        self.status = TableStatus.OCCUPIED
        self.number_of_people = number_of_people  # Define o número de pessoas
        self.orders = []  # Limpa pedidos de sessões anteriores

    def add_new_order(self, order: Order):
        """
        Adiciona um novo pedido à mesa.
        """
        if self.status != TableStatus.OCCUPIED:
            raise ValueError(f"Não é possível adicionar pedidos à Mesa {self.id}, pois ela não está ocupada.")
            
        if order.table_number != self.id:
            raise ValueError(f"O Pedido (ID: {order.id}) não pertence a esta Mesa (ID: {self.id}).")
        
        if order.status != OrderStatus.PENDING:
            raise ValueError("Só é possível adicionar pedidos com status 'Pendente' à mesa.")
            
        self.orders.append(order)

    def close_table(self) -> List[Order]:
        """
        Fecha a mesa (após o pagamento).
        Marca a mesa como disponível, zera o número de pessoas
        e retorna a lista de pedidos concluídos para arquivamento.
        """
        if self.status != TableStatus.OCCUPIED:
            raise ValueError(f"A Mesa {self.id} não está ocupada.")

        # Regra de Negócio: Não pode fechar a mesa com pedidos pendentes ou em preparo
        pending_orders = [
            order.id for order in self.orders 
            if order.status in [OrderStatus.PENDING, OrderStatus.IN_PROGRESS]
        ]
        
        if pending_orders:
            raise ValueError(f"Não é possível fechar a Mesa {self.id}. Pedidos pendentes: {pending_orders}")

        completed_orders = [
            order for order in self.orders 
            if order.status == OrderStatus.COMPLETED
        ]
        
        # Limpa a mesa para a próxima sessão
        self.status = TableStatus.AVAILABLE
        self.number_of_people = 0  # Zera o número de pessoas
        self.orders = []
        
        return completed_orders