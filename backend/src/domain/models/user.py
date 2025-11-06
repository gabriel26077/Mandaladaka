from dataclasses import dataclass
from enum import Enum
from typing import List


# --- Enum para os Papéis (Roles) ---
class UserRole(str, Enum):
    """Define os papéis (roles) possíveis para um usuário."""
    ADMIN = 'admin'
    WAITER = 'waiter'


@dataclass
class User:
    """
    Representa um Usuário no nosso domínio de negócio.
    Utiliza uma lista de 'roles' para gerenciar permissões.
    """
    id: int
    username: str  # Usado para login
    name: str      # Nome de exibição
    hashed_password: str  # O domínio nunca deve saber a senha em texto puro
    roles: List[UserRole]

    def is_admin(self) -> bool:
        """Verifica se o usuário tem o papel de ADMIN."""
        return UserRole.ADMIN in self.roles

    def is_waiter(self) -> bool:
        """Verifica se o usuário tem o papel de WAITER."""
        return UserRole.WAITER in self.roles