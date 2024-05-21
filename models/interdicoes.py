import peewee
from peewee import ForeignKeyField
from uuid import uuid4
from datetime import datetime
import werkzeug
from config import BaseModel
from models.user import Usuario

class Interdicoes(BaseModel):
    id = peewee.UUIDField(primary_key=True, default=uuid4)
    tipo = peewee.CharField()
    cep = peewee.CharField(max_length=8)
    logradouro = peewee.CharField()
    numero = peewee.CharField()
    bairro = peewee.CharField()
    cidade = peewee.CharField()
    estado = peewee.CharField()
    data = peewee.DateField()
    descricao = peewee.CharField()
    usuario = ForeignKeyField(Usuario, backref='eventos')

    def serialize(self):
        usuario_data = None
        try:
            usuario_data = {
              'id': str(self.usuario.id),
              'nome': self.usuario.nome,
              'sobrenome': self.usuario.sobrenome,
              'cpf': self.usuario.cpf,
              'whatsapp': self.usuario.whatsapp,
              'email': self.usuario.email,
            }
        except peewee.DoesNotExist:
            usuario_data = {
              'id': None,
              'nome': 'Usuário não encontrado',
              'sobrenome': 'Usuário não encontrado',
              'cpf': 'Usuário não encontrado',
              'whatsapp': 'Usuário não encontrado',
              'email': 'Usuário não encontrado',
            }
        
        return {
          'id': str(self.id),
          'usuario': usuario_data,
          'tipo': self.tipo,
          'descricao': self.descricao,
          'data_inicio': self.data,
        }

    @classmethod
    def criar(cls, tipo, cep, logradouro, numero, bairro, cidade, estado, data, descricao, usuario):
        if not tipo or not cep or not logradouro or not numero or not bairro or not cidade or not estado or not data or not descricao or not usuario:
            raise werkzeug.exceptions.BadRequest('Erro: Todos os campos obrigatórios devem ser preenchidos.')
        
        try:
          data = datetime.strptime(data, '%Y-%m-%d').date()

          nova_interdicao = cls.create(
              tipo=tipo,
              cep=cep,
              logradouro=logradouro,
              numero=numero,
              bairro=bairro,
              cidade=cidade,
              estado=estado,
              data=data,
              descricao=descricao,
              usuario=usuario
          )
          print('Interdição criada com sucesso!')
          return nova_interdicao
        except Exception as e:
          raise werkzeug.exceptions.BadRequest(f'Erro ao criar interdição: {str(e)}')

    @classmethod
    def buscar_por_tipo(cls, tipo):
      interdicoes_por_tipo = cls.select().where(cls.tipo == tipo)
      return interdicoes_por_tipo

    @classmethod
    def listar(cls):
      interdicoes = cls.select().order_by(cls.data.desc())
      return interdicoes

    @classmethod
    def deletar(cls, interdicao_id):
      try:
        interdicao = cls.get_by_id(interdicao_id)
        interdicao.delete_instance()
        print(f'Interdição com ID {interdicao_id} deletada com sucesso.')
      except cls.DoesNotExist:
        raise werkzeug.exceptions.NotFound(f'Interdição com ID {interdicao_id} não encontrada.')
      except peewee.DoesNotExist:
        raise werkzeug.exceptions.NotFound('Usuário associado à interdição não encontrado.')
