from typing import Dict, Any

# Importa as PORTAS (abstrações) do domínio
from domain.ports.product_repository import ProductRepositoryPort
from domain.ports.user_repository import UserRepositoryPort

# Importa os Modelos e Exceções
from domain.models import Product
from domain.exceptions import (
    UserNotFoundException, 
    ProductNotFoundException, 
    BusinessRuleException
)


class UpdateProductUseCase:
    """
    Caso de uso para um Admin atualizar um produto existente.
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

    def execute(
        self, 
        admin_id: int, 
        product_id: int, 
        update_data: Dict[str, Any]
    ) -> Product:
        """
        Executa a lógica de atualização do produto.
        
        Args:
            admin_id: O ID do usuário (admin) que está executando a ação.
            product_id: O ID do produto a ser atualizado.
            update_data: Um dicionário com os campos a serem atualizados.
                         Ex: {"price": 29.99, "availability": false}
            
        Returns:
            O objeto Product atualizado.
            
        Raises:
            UserNotFoundException: Se o ID do admin não for encontrado.
            ProductNotFoundException: Se o ID do produto não for encontrado.
            BusinessRuleException: Se o usuário não for admin, ou se
                                   os dados do produto forem inválidos.
        """
        
        # 1. Autorização: Verificar se o usuário é um admin
        admin_user = self.user_repository.find_by_id(admin_id)
        if not admin_user:
            raise UserNotFoundException(f"Usuário {admin_id} não encontrado.")
        
        if not admin_user.is_admin():
            raise BusinessRuleException(
                f"Usuário {admin_user.name} não tem permissão para atualizar produtos."
            )

        # 2. Buscar a entidade a ser atualizada
        product = self.product_repository.find_by_id(product_id)
        if not product:
            raise ProductNotFoundException(f"Produto {product_id} não encontrado.")

        # 3. Aplicar as atualizações (com validação)
        try:
            for key, value in update_data.items():
                if hasattr(product, key):
                    # Validação de regras de negócio
                    if key == "price" and float(value) <= 0:
                        raise ValueError("O preço deve ser positivo.")
                    if key == "name" and not value:
                        raise ValueError("O nome do produto é obrigatório.")
                    
                    # Atualiza o atributo no objeto
                    setattr(product, key, value)
                else:
                    # Ignora chaves desconhecidas para evitar erros
                    pass 

        except (ValueError, TypeError) as e:
            # Captura erros de tipo (ex: 'price' como string) ou de valor
            raise BusinessRuleException(f"Dado de atualização inválido: {e}")

        # 4. Persistir a entidade "suja"
        updated_product = self.product_repository.save(product)
        
        # 5. Retornar a entidade atualizada
        return updated_product