class DomainException(Exception):
    """
    Classe base para exceções específicas do domínio de negócio.
    Permite que as camadas superiores (aplicação, API) capturem
    erros de domínio de forma genérica.
    """
    def __init__(self, message: str):
        super().__init__(message)


class InvalidCredentialsException(DomainException):
    """
    Lançada quando as credenciais (usuário/senha) fornecidas
    durante o login são inválidas.
    """
    def __init__(self, message: str = "Credenciais inválidas."):
        super().__init__(message)


class UserNotFoundException(DomainException):
    """
    Lançada quando um usuário específico não é encontrado no repositório.
    """
    def __init__(self, message: str = "Usuário não encontrado."):
        super().__init__(message)


class ProductNotFoundException(DomainException):
    """
    Lançada quando um produto específico não é encontrado.
    """
    def __init__(self, message: str = "Produto não encontrado."):
        super().__init__(message)


class TableNotFoundException(DomainException):
    """
    Lançada quando uma mesa específica não é encontrada.
    """
    def __init__(self, message: str = "Mesa não encontrada."):
        super().__init__(message)


class OrderNotFoundException(DomainException):
    """
    Lançada quando um pedido específico não é encontrado.
    """
    def __init__(self, message: str = "Pedido não encontrado."):
        super().__init__(message)

class BusinessRuleException(DomainException):
    """
    Lançada quando uma regra de negócio é violada.
    (Ex: Tentar adicionar item a um pedido 'COMPLETED').
    
    Usamos esta exceção para erros que vêm da lógica
    nos seus Modelos (ex: order.add_item()).
    """
    def __init__(self, message: str):
        super().__init__(message)