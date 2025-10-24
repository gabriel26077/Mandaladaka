from flask import Blueprint, jsonify
import mysql.connector
from mysql.connector import Error

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return jsonify({"mensagem": "Mandaladaka API rodando"})

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '0402',
    'database': 'mdk_db'
}

def create_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

@main.route('/api/products', methods=['GET'])
def get_products():
    connection = create_db_connection()
    if connection is None:
        return jsonify({"error": "Não foi possível conectar ao banco de dados"}), 500

    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT id,name,price,availability,category,imageUrl FROM products WHERE visibility = TRUE"
        cursor.execute(query)
        products = cursor.fetchall()
        return jsonify(products)

    except Error as e:
        print(f"Erro ao buscar produtos: {e}")
        return jsonify({"error": "Erro ao buscar produtos"}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

