from flask import Blueprint, jsonify
from dataclasses import asdict  # Importante para converter dataclasses em dict

# 1. O Blueprint é criado, mas as rotas serão definidas 
#    dentro da função "fábrica"
main = Blueprint("main", __name__)

def create_main_blueprint(get_products_use_case):
    """
    Esta é uma "fábrica" que cria e configura o Blueprint.
    Ela RECEBE o(s) caso(s) de uso que precisa (Injeção de Dependência).
    """

    @main.route("/")
    def home():
        return jsonify({"mensagem": "Mandaladaka API rodando"})

    @main.route('/api/products', methods=['GET'])
    def get_products():
        # 2. Toda a lógica de banco de dados sumiu!
        
        try:
            # 3. Chama o método "execute" do caso de uso injetado
            products_list = get_products_use_case.execute()
            
            # 4. Converte a lista de objetos Product para uma lista
            #    de dicionários que pode ser "jsonifyda"
            products_dict = [asdict(p) for p in products_list]
            
            return jsonify(products_dict)

        except Exception as e:
            # Um tratamento de erro genérico para a camada web
            print(f"Erro na rota get_products: {e}")
            return jsonify({"error": "Erro ao processar requisição"}), 500
    
    # 5. A fábrica retorna o blueprint configurado
    return main