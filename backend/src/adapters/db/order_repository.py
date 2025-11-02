import mysql.connector
from mysql.connector import Error
from typing import List, Optional, Dict
from datetime import datetime

# Importa as PORTAS (Interface)
from domain.ports.order_repository import OrderRepositoryPort

# Importa os MODELOS de domínio
from domain.models import Order, OrderStatus, ItemOrder, Product

# Importa o POOL de conexões
from .connection_pool import connection_pool

class MySQLOrderRepository(OrderRepositoryPort):
    """
    Implementação CONCRETA da OrderRepositoryPort.
    Gerencia a complexidade de salvar o Agregado (Order + ItemOrders).
    """
    
    def __init__(self):
        self.pool = connection_pool

    # --- Funções de Mapeamento (Tradução DB -> Domínio) ---

    def _row_to_order_base(self, row: dict) -> Order:
        """Converte uma linha da tabela 'orders' para um objeto Order (sem itens)."""
        return Order(
            id=row['id'],
            table_number=row['table_number'],
            status=OrderStatus(row['status']), # Converte string "pending" para Enum
            created_at=row['created_at'],
            items=[] # A lista de itens será preenchida depois
        )

    def _row_to_item_with_product(self, row: dict) -> ItemOrder:
        """
        Converte uma linha (JOIN de order_items + products) 
        em um objeto ItemOrder (que contém um objeto Product).
        """
        # 1. Recria o objeto Product aninhado
        product = Product(
            id=row['product_id'],
            name=row['product_name'],
            price=float(row['product_price']),
            availability=bool(row['product_availability']),
            category=row['product_category'],
            imageUrl=row['product_imageUrl'],
            visibility=bool(row['product_visibility'])
        )
        
        # 2. Recria o objeto ItemOrder
        return ItemOrder(
            product=product,
            quantity=row['quantity']
        )
    
    # --- Implementação dos Métodos da Porta (Leitura) ---

    def find_by_id(self, order_id: int) -> Optional[Order]:
        query_order = "SELECT * FROM orders WHERE id = %s"
        query_items = """
            SELECT 
                oi.quantity,
                p.id as product_id,
                p.name as product_name,
                p.price as product_price,
                p.availability as product_availability,
                p.category as product_category,
                p.imageUrl as product_imageUrl,
                p.visibility as product_visibility
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
        """
        
        try:
            with self.pool.get_connection() as connection:
                with connection.cursor(dictionary=True) as cursor:
                    
                    # 1. Busca o Pedido (Order) principal
                    cursor.execute(query_order, (order_id,))
                    order_row = cursor.fetchone()
                    
                    if not order_row:
                        return None # Pedido não encontrado
                        
                    # 2. Converte a linha para o objeto Order (base)
                    order = self._row_to_order_base(order_row)
                    
                    # 3. Busca os Itens + Produtos associados
                    cursor.execute(query_items, (order_id,))
                    item_rows = cursor.fetchall()
                    
                    # 4. Converte e aninha os Itens no Pedido
                    for item_row in item_rows:
                        item = self._row_to_item_with_product(item_row)
                        order.items.append(item)
                        
                    return order

        except Error as e:
            print(f"Erro ao buscar pedido por ID {order_id}: {e}")
            return None

    def find_by_status(self, status: OrderStatus) -> List[Order]:
        orders_map: Dict[int, Order] = {} # { order_id -> Order_Object }
        
        query_orders = "SELECT * FROM orders WHERE status = %s"
        query_items = """
            SELECT 
                oi.order_id, oi.quantity,
                p.id as product_id, p.name as product_name, p.price as product_price,
                p.availability as product_availability, p.category as product_category,
                p.imageUrl as product_imageUrl, p.visibility as product_visibility
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id IN %s
        """ # O %s será um tupla de IDs (id1, id2, ...)

        try:
            with self.pool.get_connection() as connection:
                with connection.cursor(dictionary=True) as cursor:
                    
                    # 1. Busca todos os Pedidos (base) com o status
                    cursor.execute(query_orders, (status.value,))
                    order_rows = cursor.fetchall()
                    
                    if not order_rows:
                        return [] # Nenhum pedido encontrado
                    
                    # 2. Cria os objetos Order (base) e os mapeia por ID
                    for row in order_rows:
                        order = self._row_to_order_base(row)
                        orders_map[order.id] = order
                    
                    # 3. Busca TODOS os itens para TODOS os pedidos encontrados de uma só vez
                    order_ids = tuple(orders_map.keys())
                    cursor.execute(query_items, (order_ids,))
                    item_rows = cursor.fetchall()
                    
                    # 4. "Costura" os itens nos seus respectivos pedidos
                    for item_row in item_rows:
                        item = self._row_to_item_with_product(item_row)
                        order_id = item_row['order_id']
                        orders_map[order_id].items.append(item)
                        
                    return list(orders_map.values())

        except Error as e:
            print(f"Erro ao buscar pedidos por status {status.value}: {e}")
            return []

    # --- Implementação dos Métodos da Porta (Escrita) ---

    def save(self, order: Order) -> Order:
        """
        Salva o agregado (Order + ItemOrders) dentro de uma TRANSAÇÃO.
        """
        try:
            # Pega uma conexão para a transação
            with self.pool.get_connection() as connection:
                
                # Inicia a transação
                connection.start_transaction()
                
                try:
                    with connection.cursor() as cursor:
                        
                        # --- Passo 1: Salvar o Order principal ---
                        if order.id == 0: # INSERT
                            order_query = """
                                INSERT INTO orders (table_number, status, created_at,waiter_id) 
                                VALUES (%s, %s, %s, %s)
                            """
                            order_params = (
                                order.table_number, 
                                order.status.value, # Converte Enum para string
                                order.created_at,
                                order.waiter_id
                            )
                            cursor.execute(order_query, order_params)
                            order.id = cursor.lastrowid # Atualiza o ID no objeto
                        
                        else: # UPDATE
                            order_query = """
                                UPDATE orders SET table_number = %s, status = %s 
                                WHERE id = %s
                            """
                            order_params = (
                                order.table_number, 
                                order.status.value, 
                                order.id
                            )
                            cursor.execute(order_query, order_params)

                        # --- Passo 2: Salvar os ItemOrders ---
                        
                        # 2a. Primeiro, limpa os itens antigos (maneira mais simples de sincronizar)
                        cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order.id,))
                        
                        # 2b. Insere os itens atuais (se houver)
                        if order.items:
                            item_query = """
                                INSERT INTO order_items (order_id, product_id, quantity, price_at_order) 
                                VALUES (%s, %s, %s, %s)
                            """
                            # Cria uma lista de tuplas para o 'executemany'
                            items_data = [
                                (
                                    order.id, 
                                    item.product.id, 
                                    item.quantity,
                                    item.product.price # Salva o preço do produto no momento
                                ) 
                                for item in order.items
                            ]
                            cursor.executemany(item_query, items_data)

                    # --- Passo 3: Finalizar a Transação ---
                    connection.commit()
                    return order

                except Error as e:
                    # Se qualquer passo falhar, desfaz tudo
                    print(f"Erro durante a transação do pedido {order.id}. (ROLLBACK)")
                    connection.rollback()
                    raise e # Relança o erro para o caso de uso

        except Error as e:
            print(f"Erro ao obter conexão para salvar pedido: {e}")
            raise e