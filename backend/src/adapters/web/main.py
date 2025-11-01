import os # Importe 'os' temporariamente para a remoção segura do sys.path, mas é melhor removê-lo se não for usado.
from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException # Para tratar erros do abort()

# 1. Importa o "cérebro": o container de dependências já pronto
from .deps import container

# 2. Importa as "fábricas" de rotas
from .routers.auth_router import create_auth_blueprint
from .routers.admin_router import create_admin_blueprint
from .routers.waiter_router import create_waiter_blueprint
from .routers.kitchen_router import create_kitchen_blueprint
# (Nota: Seu blueprint 'main' antigo de 'routes.py' também entraria aqui)


# --- Criação da Aplicação ---

def create_app():
    """
    Fábrica principal da aplicação Flask.
    """
    
    app = Flask(__name__)
    
    # Habilita o CORS para permitir que o frontend acesse a API
    CORS(app) 
    
    # --- Injeção de Dependência e Registro de Rotas ---
    
    print(">>> Conectando dependências e registrando blueprints...")
    
    # Cria o blueprint de Autenticação
    auth_bp = create_auth_blueprint(
        login_uc=container.login_uc,
        get_auth_user_uc=container.get_auth_user_uc
    )
    
    # Cria o blueprint de Admin
    admin_bp = create_admin_blueprint(
        create_product_uc=container.create_product_uc,
        update_product_uc=container.update_product_uc,
        list_all_products_uc=container.list_all_products_uc,
        create_user_uc=container.create_user_uc,
        update_user_uc=container.update_user_uc
    )
    
    # Cria o blueprint do Garçom
    waiter_bp = create_waiter_blueprint(
        list_tables_uc=container.list_tables_uc,
        open_table_uc=container.open_table_uc,
        get_table_details_uc=container.get_table_details_uc,
        close_table_uc=container.close_table_uc,
        create_order_uc=container.create_order_uc,
        add_item_to_order_uc=container.add_item_to_order_uc,
        get_visible_products_uc=container.get_visible_products_uc
    )
    
    # Cria o blueprint da Cozinha
    kitchen_bp = create_kitchen_blueprint(
        list_pending_orders_uc=container.list_pending_orders_uc,
        start_order_preparation_uc=container.start_order_prep_uc,
        complete_order_preparation_uc=container.complete_order_prep_uc
    )
    
    # Registra todos os blueprints na aplicação
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(waiter_bp)
    app.register_blueprint(kitchen_bp)

    # --- Tratador de Erros Global ---
    # (Converte erros do abort() em respostas JSON)
    
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """
        Retorna respostas JSON para erros HTTP (ex: 404, 403, 401).
        """
        response = e.get_response()
        response.data = jsonify({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }).data
        response.content_type = "application/json"
        return response

    # Rota de "saúde"
    @app.route("/")
    def home():
        return jsonify({"status": "Mandaladaka API rodando!"})
        
    print(">>> Aplicação criada com sucesso.")
    return app

# --- Ponto de Entrada para Execução ---

if __name__ == "__main__":
    # O 'connection_pool' é criado no 'deps.py'
    # assim que este arquivo é executado.
    
    app = create_app()
    
    # Inicia o servidor de desenvolvimento
    # Em produção, use um servidor WSGI (Gunicorn, Waitress)
    app.run(debug=True, host="0.0.0.0", port=5000)
