from typing import Dict, Any

# Importa as PORTAS (abstrações) do domínio
from domain.ports.product_repository import ProductRepositoryPort
from domain.ports.user_repository import UserRepositoryPort

# Importa os Modelos e Exceções
from domain.models import Product
from domain.exceptions import UserNotFoundException, BusinessRuleException


class CreateProductUseCase:
    """
    Caso de uso para um Admin criar um novo produto no cardápio.
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

    def execute(self, admin_id: int, product_data: Dict[str, Any]) -> Product:
        """
        Executa a lógica de criação do produto.
        
        Args:
            admin_id: O ID do usuário (admin) que está executando a ação.
            product_data: Um dicionário com os dados do novo produto:
                {
                    "name": str,
                    "price": float,
                    "category": str,
                    "imageUrl": str,
                    "availability": bool,
                    "visibility": bool
                }
            
        Returns:
            O objeto Product recém-criado (com seu ID do banco).
            
        Raises:
            UserNotFoundException: Se o ID do admin não for encontrado.
            BusinessRuleException: Se o usuário não for admin, ou se
                                   os dados do produto forem inválidos.
        """
        
        # 1. Autorização: Verificar se o usuário é um admin
        admin_user = self.user_repository.find_by_id(admin_id)
        if not admin_user:
            raise UserNotFoundException(f"Usuário {admin_id} não encontrado.")
        
        if not admin_user.is_admin():
            raise BusinessRuleException(
                f"Usuário {admin_user.name} não tem permissão para criar produtos."
            )

        # 2. Validação de Dados
        price = product_data.get("price", 0)
        if price <= 0:
            raise BusinessRuleException("O preço do produto deve ser positivo.")
        
        if not product_data.get("name"):
            raise BusinessRuleException("O nome do produto é obrigatório.")

        # 3. Criar a entidade em memória
        try:
            new_product = Product(
                id=0,  # '0' ou 'None' para indicar "novo"
                name=product_data["name"],
                price=product_data["price"],
                category=product_data.get("category", "Sem Categoria"),
                imageUrl=product_data.get("imageUrl", ""),
                availability=product_data.get("availability", True),
                visibility=product_data.get("visibility", True)
            )
        except KeyError as e:
            raise BusinessRuleException(f"Campo obrigatório ausente: {e}")

        # 4. Persistir a nova entidade
        created_product = self.product_repository.save(new_product)
        
        # 5. Retornar a entidade criada (agora com ID)
        return created_product