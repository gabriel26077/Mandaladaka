import mysql.connector
from mysql.connector import Error
from typing import List

# Importa a abstração (Porta) que ele deve implementar
from domain.ports.product_repository import AbstractProductRepository

# Importa o modelo de domínio que ele deve retornar
from domain.models.product import Product

# Importa a configuração
from .db_config import db_config

class MySQLProductRepository(AbstractProductRepository):
    """
    Implementação CONCRETA da porta AbstractProductRepository
    usando MySQL.
    """
    
    def _create_connection(self):
        """Função utilitária para criar a conexão."""
        try:
            connection = mysql.connector.connect(**db_config)
            return connection
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def get_visible_products(self) -> List[Product]:
        """
        Implementação do método da porta.
        Ele busca dados do MySQL e os converte em objetos Product.
        """
        connection = self._create_connection()
        if connection is None:
            return []  # Retorna lista vazia se a conexão falhar

        cursor = connection.cursor(dictionary=True)
        products_list = [] # Lista para guardar os OBJETOS Product
        
        try:
            # A query original do seu routes.py
            query = "SELECT id,name,price,availability,category,imageUrl FROM products WHERE visibility = TRUE"
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Converte cada linha (dicionário) em um objeto Product
            for row in results:
                products_list.append(Product(**row))
                
            return products_list

        except Error as e:
            print(f"Erro ao buscar produtos: {e}")
            return [] # Retorna lista vazia em caso de erro
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()