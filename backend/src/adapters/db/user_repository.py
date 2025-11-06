import mysql.connector
import json # Usaremos para converter a lista de 'roles'
from mysql.connector import Error
from typing import List, Optional

# Importa a PORTA (Interface) que esta classe implementa
from domain.ports.user_repository import UserRepositoryPort

# Importa os MODELOS de domínio (User e o Enum UserRole)
from domain.models import User, UserRole

# Importa o POOL de conexões
from .connection_pool import connection_pool

class MySQLUserRepository(UserRepositoryPort):
    """
    Implementação CONCRETA da UserRepositoryPort.
    """

    def __init__(self):
        """
        O construtor armazena uma referência ao pool de conexões.
        """
        self.pool = connection_pool

    def _row_to_user(self, row: dict) -> User:
        """
        Função utilitária para mapear uma linha do DB (dicionário)
        para o objeto de domínio User.
        """
        # ... (lógica de roles continua igual) ...
        roles_list: List[UserRole] = []
        if row['roles']:
            try:
                roles_str_list = json.loads(row['roles'])
                roles_list = [UserRole(role_str) for role_str in roles_str_list]
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Erro ao decodificar roles para user {row['id']}: {e}")

        return User(
            id=row['id'],
            username=row['username'],
            name=row['name'],
            hashed_password=row['hashed_password'],
            roles=roles_list
        )

    # --- Implementação dos Métodos da Porta ---

    def find_by_id(self, user_id: int) -> Optional[User]:
        query = "SELECT * FROM users WHERE id = %s"
        try:
            with self.pool.get_connection() as connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(query, (user_id,))
                    row = cursor.fetchone()
                    if row:
                        return self._row_to_user(row)
            return None
        except Error as e:
            print(f"Erro ao buscar usuário por ID {user_id}: {e}")
            return None

    def find_by_username(self, username: str) -> Optional[User]:
        query = "SELECT * FROM users WHERE username = %s"
        try:
            with self.pool.get_connection() as connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(query, (username,))
                    row = cursor.fetchone()
                    if row:
                        return self._row_to_user(row)
            return None
        except Error as e:
            print(f"Erro ao buscar usuário por username {username}: {e}")
            return None

    def save(self, user: User) -> User:
        """
        Salva um usuário.
        """
        # ... (lógica de roles continua igual) ...
        roles_str_list = [role.value for role in user.roles]
        roles_json = json.dumps(roles_str_list)

        if user.id == 0:
            query = """
                INSERT INTO users (username, name, hashed_password, roles)
                VALUES (%s, %s, %s, %s)
            """
            params = (
                user.username, user.name,
                user.hashed_password, roles_json
            )
        else:
            query = """
                UPDATE users SET username = %s, name = %s,
                                 hashed_password = %s, roles = %s
                WHERE id = %s
            """
            params = (
                user.username, user.name,
                user.hashed_password, roles_json, user.id
            )

        try:
            with self.pool.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    connection.commit()
                    if user.id == 0:
                        user.id = cursor.lastrowid
                    return user
        except Error as e:
            print(f"Erro ao salvar usuário (pode ser username duplicado): {e}")
            raise e