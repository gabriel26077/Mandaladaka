from abc import ABC, abstractmethod
from typing import List, Optional
from ..models import Table

class TableRepositoryPort(ABC):
    """
    Define a "Porta" (Interface) para o repositório de mesas.
    """

    @abstractmethod
    def find_by_id(self, table_id: int) -> Optional[Table]:
        """Encontra uma mesa pelo seu ID (número)."""
        pass

    @abstractmethod
    def get_all_tables(self) -> List[Table]:
        """Lista todas as mesas do restaurante."""
        pass

    @abstractmethod
    def save(self, table: Table) -> Table:
        """
        Salva o estado de uma mesa (status, nro de pessoas).
        NOTA: Este método salva APENAS a mesa, não seus pedidos.
        """
        pass