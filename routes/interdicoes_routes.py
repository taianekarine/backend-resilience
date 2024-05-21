from flask import Blueprint, request, jsonify
import werkzeug
from models.interdicoes import Interdicoes
from models.user import Usuario
from middleware import token_required
from datetime import date

interdicoes_routes = Blueprint('interdicoes_routes', __name__)

@interdicoes_routes.route('/interdicoes', methods=['POST'])
@token_required
def criar_interdicao(current_user_id):
    data_atual = date.today().strftime('%Y-%m-%d')

    dados = request.json
    usuario = Usuario.get_by_id(current_user_id)
    nova_interdicao = Interdicoes.criar(
        tipo=dados.get('tipo'),
        cep=dados.get('cep'),
        logradouro=dados.get('logradouro'),
        numero=dados.get('numero'),
        bairro=dados.get('bairro'),
        cidade=dados.get('cidade'),
        estado=dados.get('estado'),
        data=data_atual,
        descricao=dados.get('descricao'),
        usuario=usuario
    )
    if nova_interdicao:
        return 'Interdição criada com sucesso!', 201
    else:
        raise werkzeug.exceptions.BadRequest('Erro ao criar interdição.')

@interdicoes_routes.route('/interdicoes/<tipo>', methods=['GET'])
@token_required
def buscar_interdicoes_por_tipo(tipo):
    interdicoes = Interdicoes.buscar_por_tipo(tipo)
    if interdicoes:
        return jsonify({'interdicoes': [interdicao.serialize() for interdicao in interdicoes]}), 200
    else:
        raise werkzeug.exceptions.NotFound(f'Não há interdições cadastradas com o tipo {tipo}')
    
@interdicoes_routes.route('/interdicoes', methods=['GET'])
@token_required
def listar_interdicoes():
    interdicoes = Interdicoes.listar()
    if interdicoes:
        return jsonify({'interdicoes': [interdicao.serialize() for interdicao in interdicoes]}), 200
    else:
        raise werkzeug.exceptions.NotFound('Não há interdições cadastradas.')
    
@interdicoes_routes.route('/interdicoes/<interdicao_id>', methods=['DELETE'])
@token_required
def deletar_interdicao(interdicao_id):
    Interdicoes.deletar(interdicao_id)
    return 'Interdição deletada com sucesso', 200
