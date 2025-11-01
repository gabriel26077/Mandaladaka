import functools
from flask import Blueprint, jsonify, request, abort, g
from pydantic import ValidationError
from typing import List

# Importa as Exceções de Domínio para tratamento de erro
from domain.exceptions import (
    BusinessRuleException,
    UserNotFoundException, # (Para o auth)
    OrderNotFoundException
)

# Importa os Casos de Uso (que serão injetados)
from domain.use_cases.kitchen import (
    ListPendingOrdersUseCase,
    StartOrderPreparationUseCase,
    CompleteOrderPreparationUseCase
)

# Importa os Schemas (DTOs da Web) para formatar a resposta
from ..schemas import OrderResponseSchema

# Importa o decorador de autenticação base
from adapters.web.routers.auth_router import auth_required

# Cria o Blueprint com um prefixo de URL
kitchen_bp = Blueprint("kitchen", __name__, url_prefix="/kitchen")


# --- DECORADOR DE AUTORIZAÇÃO ESPECÍFICO ---

def kitchen_required(f):
    """
    Decora para verificar se o usuário está logado e tem a role 'kitchen'.
    """
    @functools.wraps(f)
    @auth_required 
    def decorated_function(*args, **kwargs):
        # Verifica se a role 'kitchen' está no 'g'
        if "kitchen" not in g.user_roles and "admin" not in g.user_roles:
            abort(403, description="Acesso negado. Requer permissão de Cozinha ou Administrador.")
        return f(*args, **kwargs)
    return decorated_function


def create_kitchen_blueprint(
    list_pending_orders_uc: ListPendingOrdersUseCase,
    start_order_preparation_uc: StartOrderPreparationUseCase,
    complete_order_preparation_uc: CompleteOrderPreparationUseCase
):
    """
    Fábrica para o Blueprint da Cozinha.
    Recebe os casos de uso por Injeção de Dependência.
    """

    @kitchen_bp.route("/orders/pending", methods=["GET"])
    # @kitchen_required # <-- Quando o TODO for implementado, use este decorador!
    def list_pending_orders():
        """
        [GET /kitchen/orders/pending] Lista todos os pedidos que estão no status 'PENDING' (aguardando preparo).
        """
        kitchen_user_id = 1 # PLACEHOLDER
        
        try:
            # 1. Chama o caso de uso
            pending_orders = list_pending_orders_uc.execute()
            
            # 2. Formata a resposta
            response_data = [
                OrderResponseSchema.model_validate(o).model_dump()
                for o in pending_orders
            ]
            return jsonify(response_data)
        
        except (UserNotFoundException, BusinessRuleException) as e:
            abort(403, description=str(e)) # 403 Forbidden
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @kitchen_bp.route("/orders/<int:order_id>/start", methods=["POST"])
    # @kitchen_required # <-- Quando o TODO for implementado, use este decorador!
    def start_order_preparation(order_id: int):
        """
        [POST /kitchen/orders/<id>/start] Muda o status de um pedido para 'IN_PROGRESS' (em preparo).
        """
        kitchen_user_id = 1 # PLACEHOLDER
        
        try:
            # 1. Chama o caso de uso para mudar o status
            updated_order = start_order_preparation_uc.execute(order_id=order_id)
            
            # 2. Formata a resposta
            response_data = OrderResponseSchema.model_validate(updated_order)
            return jsonify(response_data.model_dump()), 200
        
        except OrderNotFoundException as e:
            abort(404, description=str(e)) # 404 Not Found
        except BusinessRuleException as e:
            # Ex: "Pedido não está 'PENDING'"
            abort(409, description=str(e)) # 409 Conflict
        except (UserNotFoundException) as e:
            abort(403, description=str(e))
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    
    @kitchen_bp.route("/orders/<int:order_id>/complete", methods=["POST"])
    # @kitchen_required # <-- Quando o TODO for implementado, use este decorador!
    def complete_order_preparation(order_id: int):
        """
        [POST /kitchen/orders/<id>/complete] Muda o status de um pedido para 'READY_FOR_DELIVERY' (pronto para ser entregue).
        """
        kitchen_user_id = 1 # PLACEHOLDER
        
        try:
            # 1. Chama o caso de uso
            updated_order = complete_order_preparation_uc.execute(order_id=order_id)
            
            # 2. Formata a resposta
            response_data = OrderResponseSchema.model_validate(updated_order)
            return jsonify(response_data.model_dump()), 200
        
        except OrderNotFoundException as e:
            abort(404, description=str(e))
        except BusinessRuleException as e:
            # Ex: "Pedido não está 'IN_PROGRESS'"
            abort(409, description=str(e)) # 409 Conflict
        except (UserNotFoundException) as e:
            abort(403, description=str(e))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    

    # Retorna o blueprint configurado para o main.py registrar
    return kitchen_bp
