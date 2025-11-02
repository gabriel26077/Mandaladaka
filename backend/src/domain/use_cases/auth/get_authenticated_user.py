# Importa a PORTA (abstração) do domínio
from domain.ports.user_repository import UserRepositoryPort

# Importa o Modelo e a Exceção
from domain.models import User
from domain.exceptions import UserNotFoundException


class GetAuthenticatedUserUseCase:
    """
    Caso de uso para buscar os dados de um usuário
    já autenticado (com base no ID extraído do token).
    """
    
    def __init__(self, user_repository: UserRepositoryPort):
        """
        O construtor recebe o repositório de usuário.
        """
        self.user_repository = user_repository

    def execute(self, user_id: int) -> User:
        """
        Executa a busca pelo usuário.
        
        Args:
            user_id: O ID do usuário (que viria do token autenticado).
            
        Returns:
            O objeto User, com a senha 'hashed_password' removida por segurança.
            
        Raises:
            UserNotFoundException: Se o ID do token não 
                                   corresponder a nenhum usuário no banco.
        """
        
        # 1. Buscar o usuário no repositório
        user = self.user_repository.find_by_id(user_id)
        
        # 2. Validar se o usuário realmente existe
        if not user:
            # Isso pode acontecer se um token ainda for válido,
            # mas o usuário tiver sido excluído do banco.
            raise UserNotFoundException(
                f"Usuário com ID {user_id} não encontrado."
            )
            
        # 3. MEDIDA DE SEGURANÇA: Remover o hash da senha
        # Antes de retornar o objeto para fora da camada de aplicação,
        # garantimos que o hash nunca seja exposto.
        user.hashed_password = "" 
        
        # 4. Retornar o objeto de usuário "limpo"
        return user