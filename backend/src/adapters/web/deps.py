# --- 1. Importar todas as implementações CONCRETAS (Adaptadores) ---

# Adaptadores de Banco de Dados
from ..db import (
    MySQLProductRepository,
    MySQLUserRepository,
    MySQLOrderRepository,
    MySQLTableRepository
)

# Adaptadores de Serviço
from ..services import (
    BcryptPasswordHasher,
    JwtTokenGenerator
)

# --- 2. Importar todas as classes de CASOS DE USO ---

# Casos de Uso de Autenticação
from domain.use_cases.auth import (
    LoginUseCase,
    GetAuthenticatedUserUseCase
)

# Casos de Uso de Admin
from domain.use_cases.admin import (
    CreateProductUseCase,
    UpdateProductUseCase,
    ListAllProductsUseCase,
    CreateUserUseCase,
    UpdateUserUseCase
)

# Casos de Uso da Cozinha
from domain.use_cases.kitchen import (
    ListPendingOrdersUseCase,
    StartOrderPreparationUseCase,
    CompleteOrderPreparationUseCase
)

# Casos de Uso do Garçom
from domain.use_cases.waiter import (
    ListTablesUseCase,
    OpenTableUseCase,
    GetTableDetailsUseCase,
    CloseTableUseCase,
    CreateOrderUseCase,
    AddItemToOrderUseCase
)


class AppContainer:
    """
    Container de Injeção de Dependência.
    
    Este é o ÚNICO lugar que "sabe" qual implementação concreta
    (ex: MySQLUserRepository) está sendo usada para uma interface
    (ex: UserRepositoryPort).
    """
    
    def __init__(self):
        
        # --- 1. Instanciar Adaptadores (Folhas da Árvore) ---
        
        # Serviços
        self.password_hasher = BcryptPasswordHasher()
        self.token_generator = JwtTokenGenerator()
        
        # Repositórios
        self.user_repo = MySQLUserRepository()
        self.product_repo = MySQLProductRepository()
        self.order_repo = MySQLOrderRepository()
        self.table_repo = MySQLTableRepository()

        # --- 2. Instanciar Casos de Uso (Injetando os Adaptadores) ---
        
        # Casos de Uso de Auth
        self.login_uc = LoginUseCase(
            user_repository=self.user_repo,
            password_hasher=self.password_hasher,
            token_generator=self.token_generator
        )
        self.get_auth_user_uc = GetAuthenticatedUserUseCase(
            user_repository=self.user_repo
        )
        
        # Casos de Uso de Admin
        self.create_product_uc = CreateProductUseCase(
            product_repository=self.product_repo,
            user_repository=self.user_repo
        )
        self.update_product_uc = UpdateProductUseCase(
            product_repository=self.product_repo,
            user_repository=self.user_repo
        )
        self.list_all_products_uc = ListAllProductsUseCase(
            product_repository=self.product_repo,
            user_repository=self.user_repo
        )
        self.create_user_uc = CreateUserUseCase(
            user_repository=self.user_repo,
            password_hasher=self.password_hasher
        )
        self.update_user_uc = UpdateUserUseCase(
            user_repository=self.user_repo,
            password_hasher=self.password_hasher
        )
        
        # Casos de Uso da Cozinha
        self.list_pending_orders_uc = ListPendingOrdersUseCase(
            order_repository=self.order_repo
        )
        self.start_order_prep_uc = StartOrderPreparationUseCase(
            order_repository=self.order_repo
        )
        self.complete_order_prep_uc = CompleteOrderPreparationUseCase(
            order_repository=self.order_repo
        )
        
        # Casos de Uso do Garçom
        self.list_tables_uc = ListTablesUseCase(
            table_repository=self.table_repo
        )
        self.open_table_uc = OpenTableUseCase(
            table_repository=self.table_repo
        )
        self.get_table_details_uc = GetTableDetailsUseCase(
            table_repository=self.table_repo
        )
        self.close_table_uc = CloseTableUseCase(
            table_repository=self.table_repo
        )
        self.create_order_uc = CreateOrderUseCase( # O caso de uso corrigido
            table_repository=self.table_repo,
            product_repository=self.product_repo,
            order_repository=self.order_repo
        )
        self.add_item_to_order_uc = AddItemToOrderUseCase(
            order_repository=self.order_repo,
            product_repository=self.product_repo
        )

# --- Ponto de Entrada Global ---
# Cria uma instância única do container que o main.py irá importar.
container = AppContainer()