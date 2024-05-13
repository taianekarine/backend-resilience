from flask import Blueprint, request
import bcrypt
from models.user import Usuario

login_routes = Blueprint('login_routes', __name__)

@login_routes.route('/login', methods=['POST'])
def login():
    dados = request.json
    cpf = dados.get('cpf')
    senha = dados.get('senha')
    if cpf and senha:
        usuario = Usuario.buscar_por_cpf(cpf)
        if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
            return 'Login bem-sucedido', 200
    return 'Credenciais inválidas', 401
