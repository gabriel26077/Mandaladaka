import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente
# (Isso é feito principalmente para desenvolvimento local)
load_dotenv()

# O ideal é carregar isso de variáveis de ambiente.
# Usamos os.environ.get() para ler as variáveis.
# O segundo argumento (ex: 'localhost') é um valor padrão
# caso a variável de ambiente não seja encontrada.

db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'default_password'), # Mude o padrão se quiser
    'database': os.environ.get('DB_NAME', 'mdk_db')
}