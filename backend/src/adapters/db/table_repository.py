import mysql.connector
from mysql.connector import Error
from typing import List, Optional, Dict
from datetime import datetime

# Importa as PORTAS (Interface)
from domain.ports.table_repository import TableRepositoryPort

# Importa os MODELOS de domínio
from domain.models import (
    Table, TableStatus,
    Order, OrderStatus, 
    ItemOrder, Product
)

# Importa o POOL de conexões
from .connection_pool import connection_pool

class MySQLTableRepository(TableRepositoryPort):
    """
    Implementação CONCRETA da TableRepositoryPort.
    """
    
    def __init__(self):
        self.pool = connection_pool

    # --- Funções de Mapeamento (Tradução DB -> Domínio) ---
    # (Estas são as mesmas do OrderRepository, necessárias para
    # construir os pedidos aninhados em find_by_id)

    def _row_to_table(self, row: dict) -> Table:
        """Converte uma linha da tabela 'tables' para um objeto Table (sem pedidos)."""
        return Table(
            id=row['id'],
            status=TableStatus(row['status']), # Converte string "available" para Enum
            number_of_people=row['number_of_people'],
            orders=[] # A lista de pedidos será preenchida depois
        )

    def _row_to_order_base(self, row: dict) -> Order:
        """Converte uma linha da tabela 'orders' para um objeto Order (sem itens)."""
        return Order(
            id=row['id'],
            table_number=row['table_number'],
            status=OrderStatus(row['status']),
            created_at=row['created_at'],
            items=[]
        )

    def _row_to_item_with_product(self, row: dict) -> ItemOrder:
        """Converte uma linha (JOIN de order_items + products) em um ItemOrder."""
        product = Product(
            id=row['product_id'],
            name=row['product_name'],
            price=float(row['product_price']),
            availability=bool(row['product_availability']),
            category=row['product_category'],
            imageUrl=row['product_imageUrl'],
            visibility=bool(row['product_visibility'])
        )
        return ItemOrder(
            product=product,
            quantity=row['quantity']
        )
    
    # --- Implementação dos Métodos da Porta (Leitura) ---

    def find_by_id(self, table_id: int) -> Optional[Table]:
        """
        Busca uma mesa e todos os seus pedidos e itens associados.
        (Busca "profunda" ou "eager loading").
        """
        query_table = "SELECT * FROM tables WHERE id = %s"
        query_orders = "SELECT * FROM orders WHERE table_number = %s"
        query_items = """
            SELECT 
                oi.order_id, oi.quantity,
                p.id as product_id, p.name as product_name, p.price as product_price,
                p.availability as product_availability, p.category as product_category,
                p.imageUrl as product_imageUrl, p.visibility as product_visibility
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id IN %s
        """
        
        try:
            with self.pool.get_connection() as connection:
                with connection.cursor(dictionary=True) as cursor:
                    
                    # 1. Busca a Mesa (Table)
                    cursor.execute(query_table, (table_id,))
                    table_row = cursor.fetchone()
                    if not table_row:
                        return None # Mesa não encontrada
                    
                    table = self._row_to_table(table_row)
                    
                    # 2. Busca os Pedidos (Orders) desta mesa
                    cursor.execute(query_orders, (table_id,))
                    order_rows = cursor.fetchall()
                    if not order_rows:
                        return table # Retorna a mesa (com lista de pedidos vazia)

                    # 3. Mapeia pedidos e busca seus itens
                    orders_map: Dict[int, Order] = {}
                    for row in order_rows:
                        order = self._row_to_order_base(row)
                        orders_map[order.id] = order
                        table.orders.append(order)
                    
                    order_ids = tuple(orders_map.keys())
                    cursor.execute(query_items, (order_ids,))
                    item_rows = cursor.fetchall()
                    
                    # 4. "Costura" os itens nos seus pedidos
                    for item_row in item_rows:
                        item = self._row_to_item_with_product(item_row)
                        orders_map[item_row['order_id']].items.append(item)
                        
                    return table

        except Error as e:
            print(f"Erro ao buscar mesa por ID {table_id}: {e}")
            return None

    def get_all_tables(self) -> List[Table]:
        """
        Busca todas as mesas (sem seus pedidos).
        (Busca "rasa" ou "lazy loading").
        """
        tables_list: List[Table] = []
        query = "SELECT * FROM tables"
        
        try:
            with self.pool.get_connection() as connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    
                    for row in results:
                        tables_list.append(self._row_to_table(row))
            
            return tables_list

        except Error as e:
            print(f"Erro ao buscar todas as mesas: {e}")
            return []

    # --- Implementação dos Métodos da Porta (Escrita) ---

    def save(self, table: Table) -> Table:
        """
        Salva o estado de uma mesa (status e número de pessoas).
        
        VEJA A NOTA ABAIXO: Este método NÃO salva os pedidos em cascata.
        """
        query = """
            UPDATE tables SET status = %s, number_of_people = %s
            WHERE id = %s
        """
        params = (
            table.status.value, # Converte Enum para string
            table.number_of_people,
            table.id
        )
        
        try:
            with self.pool.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    connection.commit()
                    return table
        except Error as e:
            print(f"Erro ao salvar mesa: {e}")
            raise e