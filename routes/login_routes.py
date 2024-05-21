from flask import Blueprint, request, jsonify
import bcrypt
import jwt
import datetime
from models.user import Usuario

login_routes = Blueprint('login_routes', __name__)

SECRET_KEY = 'asjaojaodvjado'

@login_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    cpf = data.get('cpf')
    senha = data.get('senha')

    if cpf and senha:
        usuario = Usuario.buscar_por_cpf(cpf)
        if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
            payload = {'cpf': cpf, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401