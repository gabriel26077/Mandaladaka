# Este arquivo importa a "fábrica" de app do nosso pacote src
# e inicia o servidor.
# Para rodar: FLASK_APP=backend/run.py flask run

from src import create_app

app = create_app()

if __name__ == "__main__":
    # Roda o app em modo debug
    app.run(debug=True, host='0.0.0.0', port=5000)