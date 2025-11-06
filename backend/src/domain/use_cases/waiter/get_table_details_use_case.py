# Importa a PORTA (abstração) do domínio
from domain.ports.table_repository import TableRepositoryPort

# Importa o Modelo e as Exceções
from domain.models import Table
from domain.exceptions import TableNotFoundException


class GetTableDetailsUseCase:
    """
    Caso de uso para buscar todos os detalhes de uma mesa específica,
    incluindo sua lista de pedidos e conta total.
    """
    
    def __init__(self, table_repository: TableRepositoryPort):
        """
        O construtor recebe o repositório de mesas.
        """
        self.table_repository = table_repository

    def execute(self, table_id: int) -> Table:
        """
        Executa a busca pelos detalhes da mesa.
        
        Args:
            table_id: O ID (número) da mesa a ser buscada.
            
        Returns:
            O objeto Table completo. O repositório é responsável
            por garantir que a lista 'table.orders' esteja populada.
            
        Raises:
            TableNotFoundException: Se a mesa com o ID fornecido não existir.
        """
        
        # 1. Buscar a entidade "Raiz de Agregado"
        # Confiamos que a implementação de 'find_by_id'
        # trará a mesa E seus pedidos associados (eager loading).
        table = self.table_repository.find_by_id(table_id)
        
        # 2. Validar se a entidade existe
        if not table:
            raise TableNotFoundException(f"Mesa {table_id} não encontrada.")
            
        # 3. Retornar a entidade completa
        return table