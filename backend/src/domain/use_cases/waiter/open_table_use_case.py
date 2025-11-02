# Importa a PORTA (abstração) do domínio
from domain.ports.table_repository import TableRepositoryPort

# Importa o Modelo e as Exceções
from domain.models import Table
from domain.exceptions import TableNotFoundException, BusinessRuleException


class OpenTableUseCase:
    """
    Caso de uso para "abrir" uma mesa, marcando-a como ocupada
    e definindo o número de pessoas.
    """
    
    def __init__(self, table_repository: TableRepositoryPort):
        """
        O construtor recebe o repositório de mesas.
        """
        self.table_repository = table_repository

    def execute(self, table_id: int, number_of_people: int) -> Table:
        """
        Executa a lógica de negócio para abrir uma mesa.
        
        Args:
            table_id: O ID (número) da mesa a ser aberta.
            number_of_people: Quantas pessoas estão sentando.
            
        Returns:
            O objeto Table atualizado.
            
        Raises:
            TableNotFoundException: Se a mesa com o ID fornecido não existir.
            BusinessRuleException: Se a lógica de domínio falhar
                                   (ex: mesa já ocupada, 0 pessoas).
        """
        
        # 1. Buscar a entidade "Raiz de Agregado"
        table = self.table_repository.find_by_id(table_id)
        
        # 2. Validar se a entidade existe
        if not table:
            raise TableNotFoundException(f"Mesa {table_id} não encontrada.")
            
        # 3. Chamar a lógica de negócio (que está no Domínio)
        try:
            # O caso de uso "comanda" o modelo de domínio
            table.open_table(number_of_people)
            
        except ValueError as e:
            # Captura exceções de regras de negócio (ex: "Mesa já ocupada")
            # e as transforma em exceções de domínio mais limpas.
            raise BusinessRuleException(str(e))
            
        # 4. Persistir a mudança de estado
        # O repositório salva o objeto 'table' que agora está "sujo"
        updated_table = self.table_repository.save(table)
        
        # 5. Retornar a entidade atualizada
        return updated_table