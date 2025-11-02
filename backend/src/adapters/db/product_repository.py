# import mysql.connector
from mysql.connector import Error
from typing import List, Optional

# Importa a PORTA (Interface) que esta classe implementa
from domain.ports.product_repository import ProductRepositoryPort

# Importa o MODELO de domínio (o que esta classe deve retornar)
from domain.models import Product

# Importa o POOL de conexões
from .connection_pool import connection_pool

class MySQLProductRepository(ProductRepositoryPort):
    """
    Implementação CONCRETA da ProductRepositoryPort usando 
    MySQL Connection Pooling.
    """
    
    def __init__(self):
        """
        O construtor armazena uma referência ao pool de conexões.
        """
        self.pool = connection_pool

    def _row_to_product(self, row: dict) -> Product:
        """
        Função utilitária para mapear uma linha do DB (dicionário)
        para o objeto de domínio Product.
        """
        # Trata a conversão de tipos (ex: Decimal do DB para float, 1/0 para bool)
        return Product(
            id=row['id'],
            name=row['name'],
            price=float(row['price']),
            availability=bool(row['availability']),
            category=row['category'],
            imageUrl=row['imageUrl'],
            visibility=bool(row['visibility']) # Assumindo que você adicionou este campo
        )

    # --- Implementação dos Métodos da Porta ---

    def get_visible_products(self) -> List[Product]:
        products_list = []
        # Selecionamos * para que o _row_to_product funcione
        query = "SELECT * FROM products WHERE visibility = TRUE"
        
        try:
            # Pega uma conexão "emprestada" do pool
            with self.pool.get_connection() as connection:
                # O 'with' garante que o cursor será fechado
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    
                    for row in results:
                        products_list.append(self._row_to_product(row))
            
            # O 'with' garante que a conexão será devolvida ao pool
            return products_list

        except Error as e:
            print(f"Erro ao buscar produtos visíveis: {e}")
            return [] # Retorna vazio em caso de erro

    def find_by_id(self, product_id: int) -> Optional[Product]:
        query = "SELECT * FROM products WHERE id = %s"
        
        try:
            with self.pool.get_connection() as connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(query, (product_id,))
                    row = cursor.fetchone()
                    
                    if row:
                        return self._row_to_product(row)
                    return None # Produto não encontrado

        except Error as e:
            print(f"Erro ao buscar produto por ID {product_id}: {e}")
            return None

    def get_all(self) -> List[Product]:
        products_list = []
        query = "SELECT * FROM products" # O Admin vê todos
        
        try:
            with self.pool.get_connection() as connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    
                    for row in results:
                        products_list.append(self._row_to_product(row))
            
            return products_list

        except Error as e:
            print(f"Erro ao buscar todos os produtos: {e}")
            return []

    def save(self, product: Product) -> Product:
        """
        Salva um produto. Se product.id for 0, insere um novo.
        Se product.id > 0, atualiza o existente.
        """
        if product.id == 0:
            # Lógica de INSERT
            query = """
                INSERT INTO products (name, price, availability, category, imageUrl, visibility) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                product.name, product.price, product.availability,
                product.category, product.imageUrl, product.visibility
            )
        else:
            # Lógica de UPDATE
            query = """
                UPDATE products SET name = %s, price = %s, availability = %s, 
                                   category = %s, imageUrl = %s, visibility = %s
                WHERE id = %s
            """
            params = (
                product.name, product.price, product.availability,
                product.category, product.imageUrl, product.visibility,
                product.id
            )

        try:
            with self.pool.get_connection() as connection:
                # Cursor normal, não 'dictionary=True', pois estamos escrevendo
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    connection.commit() # ESSENCIAL: Salva as mudanças no DB
                    
                    if product.id == 0:
                        # Se foi um INSERT, atualiza o objeto com o novo ID
                        product.id = cursor.lastrowid 
                    
                    return product # Retorna o objeto atualizado
        except Error as e:
            print(f"Erro ao salvar produto: {e}")
            # Em um app real, você relançaria uma exceção
            raise e