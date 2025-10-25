from flask import Flask
from .adapters.db.mysql_repository import MySQLProductRepository
from .adapters.web.routes import create_main_blueprint
from .domain.use_cases.get_visible_products import GetVisibleProductsUseCase

def create_app():
    """
    Fábrica de Aplicação (Application Factory).
    É aqui que a Injeção de Dependência acontece.
    """
    app = Flask(__name__)

    # --- INJEÇÃO DE DEPENDÊNCIA ---

    # 1. Criamos a instância do adaptador CONCRETO (o "lado de fora")
    product_repo = MySQLProductRepository()

    # 2. Criamos a instância do Caso de Uso (o "lado de dentro")
    #    e injetamos o repositório nele.
    get_products_use_case = GetVisibleProductsUseCase(repository=product_repo)

    # 3. Criamos o Blueprint (o adaptador web)
    #    e injetamos o caso de uso nele.
    main_bp = create_main_blueprint(
        get_products_use_case=get_products_use_case
    )

    # --- FIM DA INJEÇÃO ---
    
    # Registra o blueprint na aplicação Flask
    app.register_blueprint(main_bp)

    return app