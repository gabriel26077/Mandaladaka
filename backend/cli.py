import sys
import os
import getpass # Para digitar a senha de forma segura (escondida)

# --- Configuração de Caminho ---
# Adiciona a pasta 'src' ao Python path para que possamos
# importar de 'src.adapters', 'src.domain', etc.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
# -----------------------------

try:
    # 1. Importa o container (isso inicializa tudo: pool, etc.)
    from adapters.web.deps import container
    from domain.models import UserRole
    from domain.exceptions import BusinessRuleException, DomainException
except ImportError as e:
    print(f"Erro: Não foi possível carregar os módulos da aplicação.")
    print(f"Certifique-se de rodar este script da raiz ('backend/').")
    print(f"Detalhe: {e}")
    sys.exit(1)


def create_admin_user():
    """
    Função de CLI para criar um usuário administrador.
    """
    print("--- Criar Usuário Admin Mandaladaka ---")
    
    try:
        username = input("Username: ").strip()
        name = input("Nome (ex: Admin do Sistema): ").strip()
        
        while True:
            password = getpass.getpass("Senha (mín 6 caracteres): ")
            if len(password) < 6:
                print("Senha muito curta. Tente novamente.")
                continue
            password_confirm = getpass.getpass("Confirme a senha: ")
            if password != password_confirm:
                print("As senhas não batem. Tente novamente.")
            else:
                break
        

        user_data = {
            "username": username,
            "name": name,
            "password": password,
            "roles": [UserRole.ADMIN.value] # Converte o Enum para string
        }

        # 3. Pega o Caso de Uso do container
        create_user_uc = container.create_user_uc
        
        # 4. Executa o Caso de Uso (SEM admin_id)
        new_user = create_user_uc.execute(
            user_data=user_data,
            admin_id=None 
        )
        
        print("\n-------------------------------------------")
        print(f"✅ Sucesso! Usuário Admin '{new_user.username}' (ID: {new_user.id}) foi criado.")
        print("-------------------------------------------")

    except (BusinessRuleException, DomainException) as e:
        print(f"\n❌ Erro de Negócio: {e}")
    except (EOFError, KeyboardInterrupt):
        print("\nOperação cancelada.")
    except Exception as e:
        print(f"\n❌ Erro Inesperado: {e}")

if __name__ == "__main__":
    create_admin_user()