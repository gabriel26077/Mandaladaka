from abc import ABC, abstractmethod

class PasswordHasherPort(ABC):
    """
    Define a "Porta" (Interface) para um serviço de hash de senhas.
    Abstrai a biblioteca específica (ex: bcrypt, argon2).
    """

    @abstractmethod
    def hash(self, password_plaintext: str) -> str:
        """Gera um hash a partir de uma senha em texto puro."""
        pass

    @abstractmethod
    def check(self, password_plaintext: str, hashed_password: str) -> bool:
        """Verifica se a senha em texto puro corresponde ao hash."""
        pass