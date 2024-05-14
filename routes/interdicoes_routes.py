from flask import Blueprint, request
import werkzeug
from models.interdicoes import Interdicoes

interdicoes_routes = Blueprint('interdicoes_routes', __name__)

@interdicoes_routes.route('/interdicoes', methods=['POST'])
def criar_interdicao():
    dados = request.json
    nova_interdicao = Interdicoes.criar(**dados)
    if nova_interdicao:
        return 'Interdição criada com sucesso!', 201
    else:
      raise werkzeug.exceptions.BadRequest('Erro ao criar interdição.')


@interdicoes_routes.route('/interdicoes/<tipo>', methods=['GET'])
def buscar_interdicoes_por_tipo(tipo):
    interdicoes = Interdicoes.buscar_por_tipo(tipo)
    if interdicoes:
        return {'interdicoes': [interdicao.serialize() for interdicao in interdicoes]}, 200
    else:
        raise werkzeug.exceptions.NotFound(f'Não há interdições cadastradas com o tipo {tipo}')


@interdicoes_routes.route('/interdicoes', methods=['GET'])
def listar_interdicoes():
    interdicoes = Interdicoes.listar()
    if interdicoes:
        return {'interdicoes': [interdicao.serialize() for interdicao in interdicoes]}, 200
    else:
        raise werkzeug.exceptions.NotFound(f'Não há interdições cadastradas.')


@interdicoes_routes.route('/interdicoes/<interdicao_id>', methods=['DELETE'])
def deletar_interdicao(interdicao_id):
    Interdicoes.deletar(interdicao_id)
    return 'Interdição deletada com sucesso', 200
