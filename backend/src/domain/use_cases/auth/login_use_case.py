# Importa as ABSTRAÇÕES (Portas) do domínio
from domain.ports.user_repository import UserRepositoryPort
from domain.ports.password_hasher import PasswordHasherPort
from domain.ports.token_generator import TokenGeneratorPort

# Importa as Exceções e Modelos do domínio
from domain.exceptions import InvalidCredentialsException
from domain.models import UserRole # Necessário para o payload do token


class LoginUseCase:
    """
    Caso de uso para autenticar um usuário (Admin ou Garçom).
    """
    
    def __init__(
        self, 
        user_repository: UserRepositoryPort,
        password_hasher: PasswordHasherPort,
        token_generator: TokenGeneratorPort
    ):
        """
        O construtor recebe as dependências (Portas) de que precisa.
        """
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_generator = token_generator

    def execute(self, username: str, password_plaintext: str) -> str:
        """
        Executa a lógica de autenticação.
        
        Args:
            username: O nome de usuário fornecido.
            password_plaintext: A senha em texto puro fornecida.
            
        Returns:
            Um token de acesso (ex: JWT) como uma string.
            
        Raises:
            InvalidCredentialsException: Se o usuário não for encontrado
                                        ou a senha estiver incorreta.
        """
        
        # 1. Buscar o usuário no repositório
        user = self.user_repository.find_by_username(username)
        
        if not user:
            # Nota de Segurança: Não informe se foi o usuário ou a senha
            # que falhou. Use uma mensagem genérica.
            raise InvalidCredentialsException("Usuário ou senha inválidos.")
            
        # 2. Verificar o hash da senha usando a porta
        is_password_correct = self.password_hasher.check(
            password_plaintext=password_plaintext,
            hashed_password=user.hashed_password
        )
        
        if not is_password_correct:
            raise InvalidCredentialsException("Usuário ou senha inválidos.")
            
        # 3. Gerar e retornar o token usando a porta
        # Passamos os 'roles' para que o token possa carregá-los
        token = self.token_generator.generate(
            user_id=user.id, 
            roles=user.roles
        )
        
        return token