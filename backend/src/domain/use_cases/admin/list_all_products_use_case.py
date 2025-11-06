from typing import List

# Importa as PORTAS (abstrações) do domínio
from domain.ports.product_repository import ProductRepositoryPort
from domain.ports.user_repository import UserRepositoryPort

# Importa os Modelos e Exceções
from domain.models import Product
from domain.exceptions import UserNotFoundException, BusinessRuleException


class ListAllProductsUseCase:
    """
    Caso de uso para um Admin listar TODOS os produtos cadastrados
    (incluindo visíveis e invisíveis, disponíveis ou não).
    """
    
    def __init__(
        self, 
        product_repository: ProductRepositoryPort,
        user_repository: UserRepositoryPort
    ):
        """
        O construtor recebe os repositórios necessários.
        """
        self.product_repository = product_repository
        self.user_repository = user_repository

    def execute(self, admin_id: int) -> List[Product]:
        """
        Executa a lógica de listagem de todos os produtos.
        
        Args:
            admin_id: O ID do usuário (admin) que está executando a ação.
            
        Returns:
            Uma lista de todos os objetos Product no banco de dados.
            
        Raises:
            UserNotFoundException: Se o ID do admin não for encontrado.
            BusinessRuleException: Se o usuário não for um admin.
        """
        
        # 1. Autorização: Verificar se o usuário é um admin
        admin_user = self.user_repository.find_by_id(admin_id)
        if not admin_user:
            raise UserNotFoundException(f"Usuário {admin_id} não encontrado.")
        
        if not admin_user.is_admin():
            raise BusinessRuleException(
                f"Usuário {admin_user.name} não tem permissão para listar todos os produtos."
            )

        # 2. Chamar a porta do repositório
        # Usamos o método 'get_all()' em vez de 'get_visible_products()'
        all_products = self.product_repository.get_all()
        
        # 3. Retornar a lista completa
        return all_products