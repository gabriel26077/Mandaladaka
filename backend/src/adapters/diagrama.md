src/adapters/
│
├── __init__.py     # (Vazio)
│
├── web/            # (Adaptador Primário - "Driving")
│   │
│   ├── __init__.py
│   ├── main.py     # <-- Ponto de entrada da API (FastAPI/Flask) e Injeção de Dependência (ok)
│   ├── schemas.py  # <-- Modelos Pydantic/Marshmallow (DTOs) para entrada e saída JSON (ok)
│   ├── deps.py     # <-- (Opcional) Lógica de Injeção de Dependência (ex: "get_login_use_case") (ok)
│   │
│   └── routers/    # <-- Seus endpoints/rotas, divididos por contexto
│       ├── __init__.py (ok)
│       ├── auth_router.py    # (Rotas: /login, /me) (vamos trabalhar aqui)
│       ├── waiter_router.py  # (Rotas: /tables, /orders) ()
│       ├── kitchen_router.py # (Rotas: /kitchen/orders) ()
│       └── admin_router.py   # (Rotas: /admin/products, /admin/users) ()
│
├── db/             # (Adaptador Secundário - "Driven" - Persistência)
│   │
│   ├── __init__.py (ok)
│   ├── connection_pool.py    # (ok)
│   ├── product_repository.py # (Classe: MySQLProductRepository) (ok)
│   ├── user_repository.py    # (Classe: MySQLUserRepository) (ok)
│   ├── order_repository.py   # (Classe: MySQLOrderRepository) (ok)
│   └── table_repository.py   # (Classe: MySQLTableRepository) (ok)
│
└── services/       # (Adaptador Secundário - "Driven" - Outros Serviços)
    │
    ├── __init__.py
    └── security_service.py   # (Classes: BcryptPasswordHasher, JwtTokenGenerator) (ok)


    import functools
from flask import Blueprint, jsonify, request, abort, g
from pydantic import ValidationError
from jose import jwt, JWTError

# Importa as Exceções de Domínio para tratamento de erro
from domain.exceptions import (
    BusinessRuleException,
    UserNotFoundException,
    InvalidCredentialsException
)

# Importa os Casos de Uso (que serão injetados)
from domain.use_cases.auth import (
    LoginUseCase,
    GetAuthenticatedUserUseCase
)

# Importa os Schemas (DTOs da Web)
from ..schemas import (
    LoginSchema,
    TokenResponseSchema,
    UserResponseSchema
)

# Importa os segredos do serviço para VALIDAR tokens
from ...services.security_service import SECRET_KEY, ALGORITHM

# Cria o Blueprint com um prefixo de URL
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# --- DECORADOR DE AUTENTICAÇÃO ---
# Esta é a lógica que protege suas rotas

def auth_required(f):
    """
    Decorador para proteger rotas. Verifica o token JWT,
    valida-o e armazena o ID do usuário no 'g' (contexto global)
    do Flask para a rota usar.
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            abort(401, description="Token de autorização ausente.")
            
        parts = auth_header.split()
        
        if parts[0].lower() != "bearer" or len(parts) != 2:
            abort(401, description="Formato do token inválido (esperado: 'Bearer <token>').")
            
        token = parts[1]
        
        try:
            # 1. Valida o token (assinatura e expiração)
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            # 2. Extrai os dados do payload
            user_id = int(payload.get("sub"))
            roles = payload.get("roles", [])
            
            if not user_id:
                raise JWTError("Payload do token inválido.")
                
            # 3. Armazena os dados no contexto 'g' do Flask
            g.user_id = user_id
            g.user_roles = roles
        
        except (JWTError, ValueError, TypeError):
            abort(401, description="Token inválido, expirado ou malformado.")
        
        return f(*args, **kwargs)
    return decorated_function


# --- FÁBRICA DO BLUEPRINT ---

def create_auth_blueprint(
    login_uc: LoginUseCase,
    get_auth_user_uc: GetAuthenticatedUserUseCase
):
    """
    Fábrica para o Blueprint de Autenticação.
    Recebe os casos de uso de auth por Injeção de Dependência.
    """

    @auth_bp.route("/login", methods=["POST"])
    def login():
        json_data = request.get_json()
        if not json_data:
            abort(400, description="Nenhum dado JSON recebido.")
            
        try:
            # 1. Valida o JSON de entrada (username, password)
            validated_data = LoginSchema.model_validate(json_data)
        except ValidationError as e:
            return jsonify(e.errors()), 400
        
        try:
            # 2. Chama o caso de uso de login
            token = login_uc.execute(
                username=validated_data.username,
                password_plaintext=validated_data.password
            )
            
            # 3. Formata a resposta com o token
            response_data = TokenResponseSchema(access_token=token)
            return jsonify(response_data.model_dump()), 200
        
        except InvalidCredentialsException as e:
            # Erro de negócio (usuário/senha errados)
            abort(401, description=str(e))
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @auth_bp.route("/me", methods=["GET"])
    @auth_required  # <-- USA O DECORADOR!
    def get_current_user():
        # Se chegamos aqui, o decorador @auth_required já rodou
        # e validou o token.
        
        try:
            # 1. Pega o ID do usuário que o decorador armazenou no 'g'
            user_id = g.user_id
            
            # 2. Chama o caso de uso
            user = get_auth_user_uc.execute(user_id=user_id)
            
            # 3. Formata a resposta
            response_data = UserResponseSchema.model_validate(user)
            return jsonify(response_data.model_dump()), 200
        
        except UserNotFoundException as e:
            # Acontece se o token é válido, mas o usuário foi deletado
            abort(404, description=str(e))
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # Retorna o blueprint configurado para o main.py registrar
    return auth_bp