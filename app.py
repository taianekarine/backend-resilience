from flask import Flask
import werkzeug
from routes.user_routes import user_routes
from routes.interdicoes_routes import interdicoes_routes
from routes.login_routes import login_routes
from models.user import Usuario
from models.interdicoes import Interdicoes


app = Flask(__name__)
app.register_blueprint(user_routes)
app.register_blueprint(interdicoes_routes)
app.register_blueprint(login_routes)

def create_tables():
    # Cria as tabelas se elas não existirem
    Usuario.create_table()
    Interdicoes.create_table()

    # Comente a linha abaixo se não desejar excluir as tabelas ao iniciar o aplicativo
    # Usuario.drop_table()
    # Interdicoes.drop_table()

create_tables()

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e: Exception):
    return str(e), 400

@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_notfound_request(e: Exception):
    return str(e), 404

@app.errorhandler(werkzeug.exceptions.Unauthorized)
def handle_unauthorized_request(e: Exception):
    return str(e), 401

if __name__ == '__main__':
    app.run(port=8000, debug=True)