from typing import List, Dict, Any, Optional  # (ALTERADO) Importa Optional

# Importa as PORTAS (abstrações) do domínio
from domain.ports.user_repository import UserRepositoryPort
from domain.ports.password_hasher import PasswordHasherPort

# Importa os Modelos e Exceções
from domain.models import User, UserRole
from domain.exceptions import UserNotFoundException, BusinessRuleException


class CreateUserUseCase:
    """
    Caso de uso para um Admin criar um novo usuário (Admin ou Garçom).
    """
    
    def __init__(
        self, 
        user_repository: UserRepositoryPort,
        password_hasher: PasswordHasherPort
    ):
        """
        O construtor recebe os repositórios e serviços necessários.
        """
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    # (ALTERADO) Trocamos a ordem dos args e tornamos admin_id opcional
    def execute(self, user_data: Dict[str, Any], admin_id: Optional[int] = None) -> User:
        """
        Executa a lógica de criação do usuário.
        
        Args:
            user_data: Um dicionário com os dados do novo usuário.
            admin_id: (Opcional) O ID do usuário (admin) que está executando a ação.
                      Se None, a verificação de permissão é pulada (para CLI/Sistema).
            
        Returns:
            O objeto User recém-criado (sem o hash da senha).
            
        Raises:
            UserNotFoundException: Se o ID do admin não for encontrado.
            BusinessRuleException: Se o usuário não for admin, ou se
                                   os dados do usuário forem inválidos.
        """
        
        # (ALTERADO) Este bloco de autorização só roda se um admin_id for passado
        if admin_id is not None:
            # 1. Autorização: Verificar se o usuário é um admin
            admin_user = self.user_repository.find_by_id(admin_id)
            if not admin_user:
                raise UserNotFoundException(f"Usuário {admin_id} não encontrado.")
            
            if not admin_user.is_admin():
                raise BusinessRuleException(
                    f"Usuário {admin_user.name} não tem permissão para criar usuários."
                )

        # 2. Extrair e Validar Dados
        try:
            username = user_data["username"]
            password_plaintext = user_data["password"]
            name = user_data.get("name", "")
            roles_str = user_data.get("roles", ["waiter"])
            roles = [UserRole(role_str) for role_str in roles_str]
        except (KeyError, ValueError) as e:
            raise BusinessRuleException(f"Dados de usuário inválidos ou ausentes: {e}")
        
        if not username or not password_plaintext:
            raise BusinessRuleException("Username e password são obrigatórios.")

        # 3. Validar Regra de Negócio (Unicidade)
        if self.user_repository.find_by_username(username):
            raise BusinessRuleException(f"O username '{username}' já está em uso.")

        # 4. Chamar Serviço (Hash da Senha)
        hashed_password = self.password_hasher.hash(password_plaintext)

        # 5. Criar a entidade em memória
        new_user = User(
            id=0,
            username=username,
            name=name,
            hashed_password=hashed_password,
            roles=roles
        )

        # 6. Persistir a nova entidade
        try:
            created_user = self.user_repository.save(new_user)
        except Exception as e:
            # Captura erros do banco
            raise BusinessRuleException(f"Não foi possível salvar o usuário. {e}")
        
        # 7. Limpar e Retornar (SEGURANÇA)
        created_user.hashed_password = ""
        return created_user