
import peewee
from peewee import ForeignKeyField
from uuid import uuid4
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

  @classmethod
  def criar(cls, tipo, cep, logradouro, numero, bairro, cidade, estado, data, descricao, usuario):

    if not tipo or not cep or not logradouro or not numero or not bairro or not cidade or not estado or not data or not descricao or not usuario:
      print('Erro: Todos os campos obrigatórios devem ser preenchidos.')
      return None
    
    try:
      nova_interdicao = cls.create(
        tipo = tipo,
        cep = cep,
        logradouro = logradouro,
        numero = numero,
        bairro = bairro,
        cidade = cidade,
        estado = estado,
        data = data,
        descricao = descricao,
        usuario = usuario
      )

      print('Interdição criada com sucesso!')
      return nova_interdicao
    
    except Exception as e:
      print(f'Erro ao criar interdição: {e}')
      return None

  @classmethod
  def buscar_por_tipo(cls, tipo):
    interdicoes_por_tipo = cls.select().where(cls.tipo == tipo)
    return interdicoes_por_tipo

  @classmethod
  def listar(cls):
    return list(cls.select().order_by(cls.data.desc()))

  @classmethod
  def deletar(cls, interdicao_id):
    try:
      interdicao = cls.get_by_id(interdicao_id)
      interdicao.delete_instance()
      print(f'Interdição com ID {interdicao_id} deletada com sucesso.')

    except cls.DoesNotExist:
      print(f'Erro: Interdição com ID {interdicao_id} não encontrada.')

  