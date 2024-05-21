from flask import Blueprint, request
import werkzeug
from models.user import Usuario
from middleware import token_required

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['POST'])
def criar_usuario():
    dados = request.json
    novo_usuario = Usuario.criar(dados)
    if novo_usuario:
        return 'Usuário criado com sucesso!', 201
    else:
        raise werkzeug.exceptions.BadRequest('Erro ao criar usuário, verifique os dados inseridos.')

@user_routes.route('/users/<cpf>', methods=['GET'])
@token_required
def buscar_usuario(cpf):
    usuario = Usuario.buscar_por_cpf(cpf)
    if usuario:
        return {
            'nome': usuario.nome,
            'sobrenome': usuario.sobrenome,
            'cpf': usuario.cpf,
            'whatsapp': usuario.whatsapp,
            'email': usuario.email,
            'cep': usuario.cep,
            'logradouro': usuario.logradouro,
            'numero': usuario.numero,
            'bairro': usuario.bairro,
            'complemento': usuario.complemento,
            'cidade': usuario.cidade,
            'estado': usuario.estado
        }, 200
    else:
        raise werkzeug.exceptions.NotFound('Usuário não encontrado')

@user_routes.route('/users/<cpf>', methods=['PUT'])
@token_required
def atualizar_usuario(cpf):
    dados = request.json
    usuario_atualizado = Usuario.alterar(cpf, dados)
    if usuario_atualizado:
        return 'Usuário atualizado com sucesso', 200
    else:
        raise werkzeug.exceptions.NotFound('Não foi possivél prosseguir com a atualização dos dados do usuário.')

@user_routes.route('/users/<cpf>', methods=['DELETE'])
@token_required

def deletar_usuario(cpf):
    Usuario.deletar(cpf)
    return 'Usuário deletado com sucesso', 200
