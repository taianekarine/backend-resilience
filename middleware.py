# from werkzeug.wrappers import Request, Response

# class Middleware():
#     def __init__(self,app) :
#         self.app = app 
#         self.username ='usuario'
#         self.password = 'password'

# def __call__ (self, environ, start,response):
#     Request= Request(environ)
#     username= request.authorrizantion ['usuario']
#     password= request.authorrizantion ['password']
    
#     if username == self.username and password == self.password:
#        environ['usuario'] = {
#            'name' : 'usuario'
#        }
#        return self.app (environ, start_response)
#     res = response

from flask import request, jsonify, g
import jwt
from functools import wraps
from models.user import Usuario
import os

SECRET_KEY = os.getenv("SECRET_KEY")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            cpf = decoded_token.get('cpf')
            usuario = Usuario.buscar_por_cpf(cpf)

            if not usuario:
                return jsonify({'message': 'Invalid token'}), 401

            # Armazena o usuário no contexto global do Flask
            g.usuario = usuario

            if 'current_user_id' in f.__code__.co_varnames:
                kwargs['current_user_id'] = usuario.id

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Expired token'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated
