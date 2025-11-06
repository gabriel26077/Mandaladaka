import mysql.connector
from mysql.connector import pooling, Error

# 1. Importa a configuração do arquivo vizinho 'db_config.py'
from .db_config import db_config

try:
    # 2. Cria o Pool de Conexões UMA ÚNICA VEZ,
    #    usando a configuração importada.
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="mdk_app_pool",
        pool_size=5,  # Um bom número para começar
        **db_config   # <-- Passa o dicionário importado aqui
    )
    
    print(">>> Pool de conexões MySQL criado com sucesso.")

except Error as e:
    # 3. Se a criação do pool falhar, a aplicação não pode continuar.
    print(f"Erro fatal ao criar o pool de conexões MySQL: {e}")
    print(">>> Verifique suas variáveis de ambiente (.env) e se o banco de dados está no ar.")
    exit(1) # Encerra a aplicação se não puder conectar