from abc import ABC, abstractmethod
from typing import List
from .models.product import Product

class AbstractProductRepository(ABC):
    """
    Define a "Porta" (Interface) para o repositório de produtos.
    O domínio depende desta abstração, não de uma implementação.
    """
    
    @abstractmethod
    def get_visible_products(self) -> List[Product]:
        """Busca todos os produtos visíveis."""
        pass

    # Aqui você adicionaria outras portas, ex:
    # @abstractmethod
    # def save_product(self, product: Product) -> None:
    #     pass