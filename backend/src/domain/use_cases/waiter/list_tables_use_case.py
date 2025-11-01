from typing import List

# Importa a PORTA (abstração) do domínio
from domain.ports.table_repository import TableRepositoryPort

# Importa o Modelo que será retornado
from domain.models import Table


class ListTablesUseCase:
    """
    Caso de uso para listar todas as mesas do restaurante.
    (Visão principal do garçom).
    """
    
    def __init__(self, table_repository: TableRepositoryPort):
        """
        O construtor recebe o repositório de mesas.
        """
        self.table_repository = table_repository

    def execute(self) -> List[Table]:
        """
        Executa a busca por todas as mesas.
        
        A autenticação (verificar se o usuário está logado)
        e autorização (se é garçom ou admin) são tratadas
        pela camada de API antes de chamar este caso de uso.
        
        Returns:
            Uma lista de objetos Table, contendo o estado atual
            de todas as mesas (status, número de pessoas, etc.).
        """
        
        # 1. Chamar a porta do repositório
        tables = self.table_repository.get_all_tables()
        
        # 2. Retornar a lista
        # (Se a lista estiver vazia, retorna [], o que está correto)
        return tables