from dataclasses import dataclass, field
from typing import List
from enum import Enum
from datetime import datetime

# Importa as classes de modelos vizinhos
from .item_order import ItemOrder
from .product import Product

class OrderStatus(str, Enum):
    """
    Define os status possíveis de um Pedido.
    (Vive aqui porque está 100% acoplado ao 'Order')
    """
    PENDING = 'pending'        # Aguardando ser aceito/preparado
    IN_PROGRESS = 'in_progress'  # Em preparo na cozinha
    COMPLETED = 'completed'      # Concluído, pronto para entregar/pagar
    CANCELLED = 'cancelled'      # Cancelado

@dataclass
class Order:
    """
    Representa um Pedido (Order) no domínio.
    É uma 'Raiz de Agregado' que gerencia uma lista de ItemOrders.
    """
    # --- Atributos de Dados ---
    
    id: int
    table_number: int  # Número da mesa que fez o pedido
    waiter_id: int   # ID do garçom que atendeu a mesa
    # Um pedido pode começar vazio, por isso o default_factory
    items: List[ItemOrder] = field(default_factory=list)
    
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    
    # (Opcional: ID do usuário que criou o pedido)
    # waiter_id: int 

    # --- Propriedades (Lógica de Leitura) ---
    
    @property
    def total_price(self) -> float:
        """Calcula o preço total do pedido somando todos os itens."""
        return sum(item.total_price for item in self.items)

    # --- Métodos de Comportamento (Lógica de Escrita) ---

    def add_item(self, product: Product, quantity: int = 1):
        """
        Adiciona um produto ao pedido.
        Se o produto já existir no pedido, apenas incrementa a quantidade
        do ItemOrder existente.
        """
        # --- Regra de Negócio (Invariante) ---
        if self.status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
            raise ValueError("Não é possível adicionar itens a um pedido finalizado ou cancelado.")
            
        if quantity <= 0:
            raise ValueError("A quantidade deve ser positiva.")

        # Verifica se o item (baseado no produto) já está no pedido
        existing_item = next(
            (item for item in self.items if item.product.id == product.id), 
            None
        )
        
        if existing_item:
            # Se já existe, só adiciona a quantidade
            existing_item.add_quantity(quantity)
        else:
            # Se não existe, cria um novo ItemOrder
            new_item = ItemOrder(product=product, quantity=quantity)
            self.items.append(new_item)

    def remove_product(self, product_id: int):
        """
        Remove um produto (e seu ItemOrder correspondente) inteiramente do pedido.
        """
        # --- Regra de Negócio (Invariante) ---
        if self.status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
            raise ValueError("Não é possível remover itens de um pedido finalizado ou cancelado.")
        
        item_to_remove = next(
            (item for item in self.items if item.product.id == product_id), 
            None
        )
        
        if item_to_remove:
            self.items.remove(item_to_remove)
        else:
            # Lança um erro se tentar remover algo que não está lá
            raise ValueError(f"Produto com id {product_id} não encontrado no pedido.")

    # --- Métodos de Transição de Status (Lógica de Negócio) ---

    def mark_as_in_progress(self):
        """Muda o status do pedido para 'Em Preparo'."""
        if self.status != OrderStatus.PENDING:
            raise ValueError(f"Só é possível iniciar o preparo de pedidos 'Pendentes'. Status atual: {self.status.value}")
        self.status = OrderStatus.IN_PROGRESS

    def mark_as_completed(self):
        """Muda o status do pedido para 'Concluído'."""
        if self.status != OrderStatus.IN_PROGRESS:
            raise ValueError(f"Só é possível concluir pedidos que estão 'Em Preparo'. Status atual: {self.status.value}")
        self.status = OrderStatus.COMPLETED
        
    def mark_as_cancelled(self):
        """Muda o status do pedido para 'Cancelado'."""
        if self.status == OrderStatus.COMPLETED:
            raise ValueError("Não é possível cancelar um pedido já concluído.")
        self.status = OrderStatus.CANCELLED