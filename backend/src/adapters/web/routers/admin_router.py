import functools
from flask import Blueprint, jsonify, request, abort, g
from pydantic import ValidationError

# Importa as Exceções de Domínio
from domain.exceptions import (
    BusinessRuleException,
    UserNotFoundException,
    ProductNotFoundException
)

# Importa os Casos de Uso
from domain.use_cases.admin import (
    CreateProductUseCase,
    UpdateProductUseCase,
    ListAllProductsUseCase,
    CreateUserUseCase,
    UpdateUserUseCase
)

# Importa os Schemas
from adapters.web.schemas import (
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductResponseSchema,
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema
)

# Importa o decorador de autenticação base
from adapters.web.routers.auth_router import auth_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# Decorador de Autorização Específico para Admin
def admin_required(f):
    """
    Este decorador verifica duas coisas:
    1. Se o usuário está logado (usando @auth_required).
    2. Se o usuário logado tem a role 'admin'.
    """
    @functools.wraps(f)
    @auth_required 
    def decorated_function(*args, **kwargs):
        # 2. Verifica se a role 'admin' está no 'g'
        if "admin" not in g.user_roles:
            abort(403, description="Acesso negado. Requer permissão de administrador.")
        return f(*args, **kwargs)
    return decorated_function


def create_admin_blueprint(
    create_product_uc: CreateProductUseCase,
    update_product_uc: UpdateProductUseCase,
    list_all_products_uc: ListAllProductsUseCase,
    create_user_uc: CreateUserUseCase,
    update_user_uc: UpdateUserUseCase
):
    """
    Fábrica para o Blueprint de Admin (Versão Segura).
    """
    
    # --- ROTAS DE PRODUTO ---
    
    @admin_bp.route("/products", methods=["GET"])
    @admin_required
    def list_all_products():
        """
        [GET /admin/products] Lista todos os produtos cadastrados no sistema.
        """
        admin_id = g.user_id
        
        try:
            products = list_all_products_uc.execute(admin_id=admin_id)
            response_data = [
                ProductResponseSchema.model_validate(p).model_dump() 
                for p in products
            ]
            return jsonify(response_data)
        except (UserNotFoundException, BusinessRuleException) as e:
            abort(403, description=str(e))
    
    
    @admin_bp.route("/products", methods=["POST"])
    @admin_required
    def create_product():
        """
        [POST /admin/products] Cria um novo produto no cardápio.
        """
        admin_id = g.user_id
        
        json_data = request.get_json()
        if not json_data:
            abort(400, description="Nenhum dado JSON recebido.")
            
        try:
            validated_data = ProductCreateSchema.model_validate(json_data)
        except ValidationError as e:
            return jsonify(e.errors()), 400
        
        try:
            new_product = create_product_uc.execute(
                admin_id=admin_id,
                product_data=validated_data.model_dump()
            )
            response_data = ProductResponseSchema.model_validate(new_product)
            return jsonify(response_data.model_dump()), 201
        
        except (UserNotFoundException, BusinessRuleException) as e:
            abort(403, description=str(e))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
    
    @admin_bp.route("/products/<int:product_id>", methods=["PUT"])
    @admin_required
    def update_product(product_id: int):
        """
        [PUT /admin/products/<id>] Atualiza os dados de um produto existente.
        """
        admin_id = g.user_id
        
        json_data = request.get_json()
        if not json_data:
            abort(400, description="Nenhum dado JSON recebido.")

        try:
            validated_data = ProductUpdateSchema.model_validate(json_data)
        except ValidationError as e:
            return jsonify(e.errors()), 400
        
        try:
            updated_product = update_product_uc.execute(
                admin_id=admin_id,
                product_id=product_id,
                update_data=validated_data.model_dump(exclude_unset=True)
            )
            response_data = ProductResponseSchema.model_validate(updated_product)
            return jsonify(response_data.model_dump()), 200
        
        except ProductNotFoundException as e:
            abort(404, description=str(e))
        except (UserNotFoundException, BusinessRuleException) as e:
            abort(403, description=str(e))
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # --- ROTAS DE USUÁRIO ---

    @admin_bp.route("/users", methods=["POST"])
    @admin_required
    def create_user():
        """
        [POST /admin/users] Cria um novo usuário (admin, waiter ou kitchen).
        """
        admin_id = g.user_id
        
        json_data = request.get_json()
        if not json_data:
            abort(400, description="Nenhum dado JSON recebido.")
            
        try:
            validated_data = UserCreateSchema.model_validate(json_data)
        except ValidationError as e:
            return jsonify(e.errors()), 400
        
        try:
            new_user = create_user_uc.execute(
                admin_id=admin_id,
                user_data=validated_data.model_dump(mode="json")
            )
            response_data = UserResponseSchema.model_validate(new_user)
            return jsonify(response_data.model_dump()), 201
        
        except BusinessRuleException as e:
            abort(409, description=str(e))
        except (UserNotFoundException) as e:
            abort(403, description=str(e))
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @admin_bp.route("/users/<int:user_id>", methods=["PUT"])
    @admin_required
    def update_user(user_id: int):
        """
        [PUT /admin/users/<id>] Atualiza os dados de um usuário existente.
        """
        admin_id = g.user_id
        
        json_data = request.get_json()
        if not json_data:
            abort(400, description="Nenhum dado JSON recebido.")

        try:
            validated_data = UserUpdateSchema.model_validate(json_data)
        except ValidationError as e:
            return jsonify(e.errors()), 400
        
        try:
            updated_user = update_user_uc.execute(
                admin_id=admin_id,
                user_id_to_update=user_id,
                update_data=validated_data.model_dump(exclude_unset=True, mode="json")
            )
            response_data = UserResponseSchema.model_validate(updated_user)
            return jsonify(response_data.model_dump()), 200
        
        except UserNotFoundException as e:
            abort(404, description=str(e))
        except BusinessRuleException as e:
            abort(409, description=str(e))
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return admin_bp
