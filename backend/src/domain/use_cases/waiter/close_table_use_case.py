# Importa a PORTA (abstração) do domínio
from domain.ports.table_repository import TableRepositoryPort

# Importa o Modelo e as Exceções
from domain.models import Table
from domain.exceptions import TableNotFoundException, BusinessRuleException


class CloseTableUseCase:
    """
    Caso de uso para "fechar" uma mesa após o pagamento,
    marcando-a como disponível e zerando seus dados de sessão.
    """
    
    def __init__(self, table_repository: TableRepositoryPort):
        """
        O construtor recebe o repositório de mesas.
        """
        self.table_repository = table_repository

    def execute(self, table_id: int) -> Table:
        """
        Executa a lógica de negócio para fechar uma mesa.
        
        Args:
            table_id: O ID (número) da mesa a ser fechada.
            
        Returns:
            O objeto Table atualizado (agora com status 'AVAILABLE').
            
        Raises:
            TableNotFoundException: Se a mesa com o ID fornecido não existir.
            BusinessRuleException: Se a lógica de domínio falhar
                                   (ex: mesa já está livre, pedidos pendentes).
        """
        
        # 1. Buscar o Agregado Raiz (a Mesa)
        # Precisamos dos pedidos para a lógica de validação
        table = self.table_repository.find_by_id(table_id)
        
        # 2. Validar se a entidade existe
        if not table:
            raise TableNotFoundException(f"Mesa {table_id} não encontrada.")
            
        # 3. Chamar a lógica de negócio (que está no Domínio)
        try:
            # O caso de uso "comanda" o modelo de domínio
            # O método .close_table() fará a validação de pedidos pendentes
            # e mudará o status, o nro de pessoas e limpará a lista de pedidos.
            table.close_table()
            
        except ValueError as e:
            # Captura exceções de regras de negócio (ex: "Pedidos pendentes")
            raise BusinessRuleException(str(e))
            
        # 4. Persistir a mudança de estado
        # O repositório salva o objeto 'table' que agora está "sujo"
        updated_table = self.table_repository.save(table)
        
        # 5. Retornar a entidade atualizada
        return updated_table