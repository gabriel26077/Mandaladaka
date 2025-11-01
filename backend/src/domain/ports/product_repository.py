#domain/ports/product_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from ..models import Product # (Corrigido o import para ..models)

class ProductRepositoryPort(ABC):
    """
    Define a "Porta" (Interface) para o repositório de produtos.
    """
    
    @abstractmethod
    def get_visible_products(self) -> List[Product]:
        """Busca todos os produtos visíveis (para o cardápio)."""
        pass

    @abstractmethod
    def find_by_id(self, product_id: int) -> Optional[Product]:
        """Encontra um produto pelo seu ID."""
        pass
        
    @abstractmethod
    def get_all(self) -> List[Product]:
        """Busca TODOS os produtos (para o painel do admin)."""
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        """Salva um produto (novo ou existente)."""
        pass