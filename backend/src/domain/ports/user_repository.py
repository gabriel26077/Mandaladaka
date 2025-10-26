from abc import ABC, abstractmethod
from typing import Optional
from ..models import User

class UserRepositoryPort(ABC):
    """
    Define a "Porta" (Interface) para o repositório de usuários.
    """
    
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Encontra um usuário pelo seu ID."""
        pass

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        """Encontra um usuário pelo seu nome de usuário (para login)."""
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        """Salva um usuário (novo ou existente)."""
        pass