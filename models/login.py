import bcrypt
from models.user import Usuario
import jwt
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuração da chave secreta para o JWT
SECRET_KEY = 'asjaojaodvjado'

class Autenticacao:
    @staticmethod
    def generate_token(username):
        payload = {
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def validate_token(token):
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return decoded_token
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def login(username, password):
        user = Usuario.get(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.senha.encode('utf-8')):
            return user
        else:
            return None

@app.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    token = Autenticacao.login(username, password)
    if token:
        return jsonify({'token': token})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing'}), 401

    token = token.split(" ")[1]  # Remove o prefixo "Bearer "

    decoded_token = Autenticacao.validate_token(token)
    if decoded_token:
        return jsonify({'message': f'Welcome {decoded_token["username"]}!'})
    else:
        return jsonify({'message': 'Invalid token'}), 401

if __name__ == '_main_':
    app.run(debug=True)