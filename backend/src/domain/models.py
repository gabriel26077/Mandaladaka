# backend/src/domain/models.py

from dataclasses import dataclass

@dataclass
class Product:
    """
    Representa um Produto no nosso domínio de negócio.
    É um objeto de dados puro (DTO) usado internamente.
    """
    id: int
    name: str
    price: float
    availability: bool
    category: str
    imageUrl: str
