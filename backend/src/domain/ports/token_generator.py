from abc import ABC, abstractmethod
from typing import List
from ..models import UserRole

class TokenGeneratorPort(ABC):
    """
    Define a "Porta" (Interface) para um serviço de geração de token (ex: JWT).
    Abstrai a biblioteca específica e a 'secret key'.
    """

    @abstractmethod
    def generate(self, user_id: int, roles: List[UserRole]) -> str:
        """Gera um token de acesso para um usuário."""
        pass