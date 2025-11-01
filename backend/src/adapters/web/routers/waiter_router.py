import functools
from flask import Blueprint, jsonify, request, abort, g
from pydantic import ValidationError
from typing import List

# Importa as Exceções de Domínio para tratamento de erro
from domain.exceptions import (
    BusinessRuleException,
    UserNotFoundException,
    TableNotFoundException,
    OrderNotFoundException,
    ProductNotFoundException
)

# Importa os Casos de Uso (que serão injetados)
from domain.use_cases.waiter import (
    ListTablesUseCase,
    OpenTableUseCase,
    GetTableDetailsUseCase,
    CloseTableUseCase,
    CreateOrderUseCase,
    AddItemToOrderUseCase
)

from domain.use_cases.get_visible_products import GetVisibleProductsUseCase

# Importa os Schemas (DTOs da Web) que este router precisará
from ..schemas import (
    TableResponseSchema,
    TableDetailsResponseSchema,
    OpenTableSchema,
    OrderResponseSchema,
    CreateOrderSchema,
    AddItemToOrderSchema,
)

# Importa o decorador de autenticação base
from adapters.web.routers.auth_router import auth_required

# Cria o Blueprint. Usaremos /tables e /orders como prefixos de rota.
waiter_bp = Blueprint("waiter", __name__, url_prefix="/")





# --- DECORADOR DE AUTORIZAÇÃO ESPECÍFICO ---

def waiter_required(f):
    """
    Decora para verificar se o usuário está logado e tem a role 'waiter'.
    """
    @functools.wraps(f)
    @auth_required 
    def decorated_function(*args, **kwargs):
        # Verifica se a role 'waiter' está no 'g'
        if "waiter" not in g.user_roles and "admin" not in g.user_roles:
            abort(403, description="Acesso negado. Requer permissão de Garçom ou Administrador.")
        return f(*args, **kwargs)
    return decorated_function


def create_waiter_blueprint(
    list_tables_uc: ListTablesUseCase,
    open_table_uc: OpenTableUseCase,
    get_table_details_uc: GetTableDetailsUseCase,
    close_table_uc: CloseTableUseCase,
    create_order_uc: CreateOrderUseCase,
    add_item_to_order_uc: AddItemToOrderUseCase,
    get_visible_products_uc: GetVisibleProductsUseCase
):
    """
    Fábrica para o Blueprint do Garçom (Waiter).
    Recebe todos os casos de uso de atendimento por Injeção de Dependência.
    """

    # --- ROTAS DE MESA (TABLE) ---

    @waiter_bp.route("/tables", methods=["GET"])
    @waiter_required 
    def list_tables():
        """
        [GET /tables] Lista todas as mesas do restaurante e seus status atuais.
        """
        waiter_id = 1 # PLACEHOLDER
        
        try:
            # 1. Chama o caso de uso (que busca no db)
            tables = list_tables_uc.execute()
            
            # 2. Formata a resposta (lista de mesas "rasa")
            response_data = [
                TableResponseSchema.model_validate(t).model_dump() 
                for t in tables
            ]
            return jsonify(response_data)
        
        except (UserNotFoundException, BusinessRuleException) as e:
            abort(403, description=str(e)) # 403 Forbidden
        except Exception as e:
            return jsonify({"error": str(e)}), 500



    # No waiter_router.py, corrija a função list_available_products():
    @waiter_bp.route("/products", methods=["GET"])
    @waiter_required
    def list_available_products():
        """
        [GET /products] Lista todos os produtos disponíveis no cardápio.
        """
        try:
            # Reutiliza o caso de uso existente
            products = get_visible_products_uc.execute()
            
            # Formata a resposta
            response_data = [
                {
                    "id": p.id,
                    "name": p.name,
                    "price": float(p.price),
                    "description": p.description,
                    "category": p.category,
                    "imageUrl": p.imageUrl,
                    "availability": p.availability
                }
                for p in products
            ]
            return jsonify(response_data), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        # E REMOVA o "return waiter_bp" que está dentro da função acima
        # O return waiter_bp deve estar no FINAL da create_waiter_blueprint()



    @waiter_bp.route("/tables/<int:table_id>/open", methods=["POST"])
    @waiter_required
    def open_table(table_id: int):
        """
        [POST /tables/<id>/open] Abre uma mesa (muda o status para 'OCCUPIED').
        """
        waiter_id = 1 # PLACEHOLDER
        
        json_data = request.get_json()
        if not json_data:
            abort(400, description="Nenhum dado JSON recebido.")
            
        try:
            # 1. Valida o JSON de entrada
            validated_data = OpenTableSchema.model_validate(json_data)
        except ValidationError as e:
            return jsonify(e.errors()), 400
        
        try:
            # 2. Chama o caso de uso
            updated_table = open_table_uc.execute(
                table_id=table_id,
                number_of_people=validated_data.number_of_people
            )
            
            # 3. Formata a resposta
            response_data = TableResponseSchema.model_validate(updated_table)
            return jsonify(response_data.model_dump()), 200
        
        except TableNotFoundException as e:
            abort(404, description=str(e)) # 404 Not Found
        except BusinessRuleException as e:
            # Ex: "Mesa já ocupada"
            abort(409, description=str(e)) # 409 Conflict
        except (UserNotFoundException) as e:
            abort(403, description=str(e))
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @waiter_bp.route("/tables/<int:table_id>", methods=["GET"])
    @waiter_required
    def get_table_details(table_id: int):
        """
        [GET /tables/<id>] Busca os detalhes de uma mesa, incluindo o pedido ativo.
        """
        waiter_id = 1 # PLACEHOLDER
        
        try:
            # 1. Chama o caso de uso
            table = get_table_details_uc.execute(table_id=table_id)
            
            # 2. Formata a resposta (mesa "profunda" com pedidos)
            response_data = TableDetailsResponseSchema.model_validate(table)
            return jsonify(response_data.model_dump()), 200
        
        except TableNotFoundException as e:
            abort(404, description=str(e))
        except (UserNotFoundException, BusinessRuleException) as e:
            abort(403, description=str(e))
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @waiter_bp.route("/tables/<int:table_id>/close", methods=["POST"])
    @waiter_required
    def close_table(table_id: int):
        """
        [POST /tables/<id>/close] Fecha uma mesa. O pedido deve estar pago/concluído.
        """
        waiter_id = 1 # PLACEHOLDER
        
        try:
            # 1. Chama o caso de uso
            updated_table = close_table_uc.execute(table_id=table_id)
            
            # 2. Formata a resposta
            response_data = TableResponseSchema.model_validate(updated_table)
            return jsonify(response_data.model_dump()), 200
        
        except TableNotFoundException as e:
            abort(404, description=str(e))
        except BusinessRuleException as e:
            # Ex: "Pedidos pendentes"
            abort(409, description=str(e))
        except (UserNotFoundException) as e:
            abort(403, description=str(e))
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # --- ROTAS DE PEDIDO (ORDER) ---

    @waiter_bp.route("/tables/<int:table_id>/orders", methods=["POST"])
    @waiter_required
    def create_order_for_table(table_id: int):
        """
        [POST /tables/<id>/orders] Cria um novo pedido para uma mesa ocupada.
        """
        waiter_id = 1 # PLACEHOLDER
        
        json_data = request.get_json()
        if not json_data:
            abort(400, description="Nenhum dado JSON recebido.")
            
        try:
            # 1. Valida o JSON de entrada
            validated_data = CreateOrderSchema.model_validate(json_data)
        except ValidationError as e:
            return jsonify(e.errors()), 400
        
        try:
            # 2. Chama o caso de uso
            new_order = create_order_uc.execute(
                table_id=table_id,
                items_data=validated_data.model_dump().get("items", [])
            )
            
            # 3. Formata a resposta
            response_data = OrderResponseSchema.model_validate(new_order)
            return jsonify(response_data.model_dump()), 201
        
        except (TableNotFoundException, ProductNotFoundException) as e:
            abort(404, description=str(e))
        except BusinessRuleException as e:
            # Ex: "Mesa não está ocupada"
            abort(409, description=str(e))
        except (UserNotFoundException) as e:
            abort(403, description=str(e))
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @waiter_bp.route("/orders/<int:order_id>/items", methods=["POST"])
    @waiter_required
    def add_item_to_order(order_id: int):
        """
        [POST /orders/<id>/items] Adiciona um item a um pedido existente.
        """
        waiter_id = 1 # PLACEHOLDER
        
        json_data = request.get_json()
        if not json_data:
            abort(400, description="Nenhum dado JSON recebido.")

        try:
            # 1. Valida o JSON de entrada
            validated_data = AddItemToOrderSchema.model_validate(json_data)
        except ValidationError as e:
            return jsonify(e.errors()), 400
            
        try:
            # 2. Chama o caso de uso
            updated_order = add_item_to_order_uc.execute(
                order_id=order_id,
                product_id=validated_data.product_id,
                quantity=validated_data.quantity
            )
            
            # 3. Formata a resposta
            response_data = OrderResponseSchema.model_validate(updated_order)
            return jsonify(response_data.model_dump()), 200
        
        except (OrderNotFoundException, ProductNotFoundException) as e:
            abort(404, description=str(e))
        except BusinessRuleException as e:
            # Ex: "Pedido já está concluído"
            abort(409, description=str(e))
        except (UserNotFoundException) as e:
            abort(403, description=str(e))
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # Retorna o blueprint configurado para o main.py registrar
    return waiter_bp
