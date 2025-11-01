import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import List

# Importa as ABSTRAÇÕES (Portas) que esta classe implementa
from domain.ports.password_hasher import PasswordHasherPort
from domain.ports.token_generator import TokenGeneratorPort
from domain.models import UserRole # Necessário para o payload do token

# --- Configuração de Segurança ---
# IMPORTANTE: Em produção, NUNCA deixe valores fixos no código.
# Use variáveis de ambiente (ex: os.getenv("SECRET_KEY"))
SECRET_KEY = "sua-chave-secreta-muito-forte-aqui-mude-isso"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # 1 hora

class BcryptPasswordHasher(PasswordHasherPort):
    """
    Implementação concreta da porta de hash usando a biblioteca Bcrypt.
    """
    
    def hash(self, password_plaintext: str) -> str:
        """
        Gera um hash a partir de uma senha em texto puro.
        """
        # Converte a senha para bytes, gera o salt e o hash
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(password_plaintext.encode('utf-8'), salt)
        
        # Retorna o hash como uma string decodificada
        return hashed_bytes.decode('utf-8')

    def check(self, password_plaintext: str, hashed_password: str) -> bool:
        """
        Verifica se a senha em texto puro corresponde ao hash.
        """
        try:
            # Compara a senha (em bytes) com o hash (em bytes)
            return bcrypt.checkpw(
                password_plaintext.encode('utf-8'), 
                hashed_password.encode('utf-8')
            )
        except ValueError:
            # bcrypt.checkpw pode lançar ValueError se o hash for malformado
            return False

class JwtTokenGenerator(TokenGeneratorPort):
    """
    Implementação concreta da porta de token usando JWT (biblioteca python-jose).
    """
    
    def generate(self, user_id: int, roles: List[UserRole]) -> str:
        """
        Gera um token de acesso (JWT) para um usuário.
        """
        # Calcula o tempo de expiração
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        # Converte a lista de Enums [UserRole.ADMIN] para uma lista de strings ["admin"]
        roles_str_list = [role.value for role in roles]
        
        # 'data' é o payload (carga útil) do token
        data_to_encode = {
            "sub": str(user_id), # 'subject' (o ID do usuário) é o padrão
            "roles": roles_str_list,
            "exp": expire, # Tempo de expiração
        }
        
        # Gera o token assinado
        encoded_jwt = jwt.encode(
            data_to_encode, 
            SECRET_KEY, 
            algorithm=ALGORITHM
        )
        
        return encoded_jwt