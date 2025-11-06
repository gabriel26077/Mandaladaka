from typing import Dict, Any, Optional

# Importa as PORTAS (abstrações) do domínio (Absoluto)
from domain.ports.user_repository import UserRepositoryPort
from domain.ports.password_hasher import PasswordHasherPort

# Importa os Modelos e Exceções (Absoluto)
from domain.models import User, UserRole
from domain.exceptions import (
    UserNotFoundException,
    BusinessRuleException
)


class UpdateUserUseCase:
    """
    Caso de uso para um Admin atualizar um usuário existente.
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

    def execute(
        self,
        admin_id: int,
        user_id_to_update: int,
        update_data: Dict[str, Any]
    ) -> User:
        """
        Executa a lógica de atualização do usuário.

        Args:
            admin_id: O ID do usuário (admin) que está executando a ação.
            user_id_to_update: O ID do usuário a ser atualizado.
            update_data: Um dicionário com os campos a serem atualizados.
                         Ex: {"name": "Novo Nome", "password": "nova_senha"}

        Returns:
            O objeto User atualizado (sem o hash da senha).

        Raises:
            UserNotFoundException: Se o admin ou o usuário não forem encontrados.
            BusinessRuleException: Se o usuário não for admin, ou se
                                   os dados de atualização forem inválidos.
        """

        # 1. Autorização: Verificar se o usuário é um admin
        admin_user = self.user_repository.find_by_id(admin_id)
        if not admin_user:
            raise UserNotFoundException(f"Usuário admin {admin_id} não encontrado.")

        if not admin_user.is_admin():
            raise BusinessRuleException(
                f"Usuário {admin_user.name} não tem permissão para atualizar usuários."
            )

        # 2. Buscar a entidade a ser atualizada
        user = self.user_repository.find_by_id(user_id_to_update)
        if not user:
            raise UserNotFoundException(f"Usuário {user_id_to_update} não encontrado.")

        # 3. Aplicar as atualizações (com validação)
        try:
            for key, value in update_data.items():

                # Campos com lógica especial
                if key == "password":
                    if value: # Só atualiza a senha se ela não for vazia
                        user.hashed_password = self.password_hasher.hash(value)

                elif key == "roles":
                    # Converte a lista de strings (vindo do JSON) para Enums
                    user.roles = [UserRole(role_str) for role_str in value]

                elif key == "username":
                    if not value:
                        raise ValueError("Username não pode ser vazio.")
                    # Verifica se o username mudou e se o novo já existe
                    if value != user.username and self.user_repository.find_by_username(value):
                        raise BusinessRuleException(f"O username '{value}' já está em uso.")
                    user.username = value

                # Campos simples que existem no modelo (name)
                elif hasattr(user, key):
                    # Ignora 'id' e 'hashed_password' (tratado acima)
                    # O campo 'email' será ignorado aqui porque hasattr(user, 'email') é False
                    if key not in ["id", "hashed_password"]:
                        setattr(user, key, value)

                # Ignora chaves desconhecidas (como 'email') silenciosamente

        except (ValueError, TypeError) as e:
            # Captura erros de tipo ou valor (ex: roles não é lista, price inválido se existisse)
            raise BusinessRuleException(f"Dado de atualização inválido: {e}")
        except Exception as e:
             # Captura outros erros inesperados durante o processamento
             raise BusinessRuleException(f"Erro ao processar atualização: {e}")

        # 4. Persistir a entidade "suja"
        try:
            # O repositório já foi corrigido para não usar 'email'
            updated_user = self.user_repository.save(user)
        except Exception as e:
            # Captura erros do banco (ex: username duplicado se UNIQUE falhar)
            raise BusinessRuleException(f"Não foi possível salvar o usuário. {e}")

        # 5. Limpar e Retornar (SEGURANÇA)
        updated_user.hashed_password = ""
        return updated_user