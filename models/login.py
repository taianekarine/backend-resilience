import bcrypt
from models.user import Usuario
import jwt
import datetime
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Configuração da chave secreta para o JWT
SECRET_KEY = os.getenv("SECRET_KEY")

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

if __name__ == '_main_':
    app.run(debug=True)