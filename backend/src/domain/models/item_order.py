from dataclasses import dataclass
from .product import Product  # Importa o Product do arquivo vizinho

@dataclass
class ItemOrder:
    """
    Representa um item específico dentro de um Pedido (Order).
    
    Ele vincula um Produto (product) a uma quantidade (quantity)
    e é capaz de calcular seu próprio subtotal.
    """
    product: Product
    quantity: int

    @property
    def total_price(self) -> float:
        """
        Calcula e retorna o preço total para este item.
        (preço do produto * quantidade)
        """
        # Usamos o 'price' do objeto Product que ele contém
        return self.product.price * self.quantity

    def add_quantity(self, amount: int = 1):
        """Adiciona uma quantidade ao item."""
        if amount < 0:
            raise ValueError("A quantidade a adicionar não pode ser negativa")
        self.quantity += amount

    def remove_quantity(self, amount: int = 1):
        """Remove uma quantidade do item."""
        if amount < 0:
            raise ValueError("A quantidade a remover não pode ser negativa")
        if (self.quantity - amount) < 0:
            raise ValueError("A quantidade não pode ficar negativa")
        self.quantity -= amount