# ====================================================================
# CONFIGURACAO LOCAL (NAO RASTREADA PELO GIT)
# ====================================================================

# Verifica se o arquivo de configuracao existe. Se nao, para a execucao e avisa o usuario.
ifndef DB_NAME
    ifeq ($(wildcard config.mk),)
        $(error ERRO: Arquivo 'config.mk' nao encontrado. Copie 'config.mk.example' para 'config.mk' e preencha as variaveis locais.)
    endif
endif

include config.mk


# ====================================================================
# VARIAVEIS UTEIS
# ====================================================================

# Variaveis de diretorio (constantes no projeto)
BACKEND_DIR = backend
FRONTEND_DIR = frontend

# PYTHON_VENV_ACTIVATE, DB_NAME, DB_USER, DB_PASSWORD sao carregadas de config.mk


# ====================================================================
# COMANDOS DE INSTALACAO
# ====================================================================

# Instala as dependencias do backend (Python)
install-back:
	@echo ">>> INSTALANDO BACKEND: Criando venv e instalando dependencias..."
	# Cria o ambiente virtual
	@python -m venv $(BACKEND_DIR)/venv
	# Instala as dependencias
	@cd $(BACKEND_DIR)/ ; $(PYTHON_VENV_ACTIVATE) ; pip install -r requirements.txt
	@echo "Backend instalado com sucesso."

# Instala as dependencias do frontend (Node.js)
install-front:
	@echo ">>> INSTALANDO FRONTEND: Executando npm install..."
	@cd $(FRONTEND_DIR)/ ; npm install
	@echo "Frontend instalado com sucesso."

# Instala tudo
install-all: install-back install-front
	@echo "--- INSTALACAO COMPLETA ---"
	@echo "Voce pode inicializar o banco de dados com 'make init-db'."

# ====================================================================
# COMANDOS DE BANCO DE DADOS
# ====================================================================

init-db:
	@echo "Inicializando o banco de dados MariaDB/MySQL..."
	# Comando para MariaDB/MySQL:
	mysql -u $(DB_USER) -p$(DB_PASSWORD) $(DB_NAME) < database/init_db.sql
	@echo "Banco de dados MariaDB/MySQL inicializado com sucesso."

# ====================================================================
# COMANDOS DE EXECUCAO
# ====================================================================

# Inicia o backend (Flask) em PRIMEIRO PLANO.
run-back:
	@echo ">>> INICIANDO BACKEND (Terminal 1) <<<"
	@cd $(BACKEND_DIR) ;  $(PYTHON_VENV_ACTIVATE) ; cd src ; python -m adapters.web.main
	
# Inicia o frontend (Next.js) em PRIMEIRO PLANO.
run-front:
	@echo ">>> INICIANDO FRONTEND (Terminal 2) <<<"
	@cd $(FRONTEND_DIR)/ ; npm run dev

# Comando de execucao completa (Apenas uma instrucao)
help:
	@echo "--- PROCESSO DE INICIALIZACAO DO SISTEMA ---"
	@echo "1. Configure 'config.mk'."
	@echo "2. Instale dependencias: make install-all"
	@echo "3. (Opcional) Inicialize o banco: make init-db"
	@echo "4. Abra um terminal e execute: make run-back"
	@echo "5. Abra outro terminal e execute: make run-front"
	@echo "Pressione Ctrl+C em cada terminal para encerrar o respectivo servico."

# ====================================================================
# METADADOS
# ====================================================================

.PHONY: run-front run-back help init-db install-back install-front install-all