from typing import List
from ..models import Product
from ..ports import AbstractProductRepository

class GetVisibleProductsUseCase:
    """
    Representa o caso de uso de negócio para buscar produtos visíveis.
    """
    def __init__(self, repository: AbstractProductRepository):
        # O caso de uso recebe a ABSTRAÇÃO do repositório
        self.repository = repository

    def execute(self) -> List[Product]:
        """
        Executa a lógica de negócio.
        (Neste caso, é simples, mas poderia ter filtros, regras, etc.)
        """
        products = self.repository.get_visible_products()
        return products