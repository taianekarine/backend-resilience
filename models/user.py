import bcrypt
import peewee
from peewee import DoesNotExist
from uuid import uuid4

import werkzeug
from config import BaseModel

class Usuario(BaseModel):
    id = peewee.UUIDField(primary_key=True, default=uuid4)
    nome = peewee.CharField()
    sobrenome = peewee.CharField()
    cpf = peewee.CharField(unique=True, max_length=11)
    whatsapp = peewee.CharField()
    email = peewee.CharField(unique=True)
    senha = peewee.CharField()
    cep = peewee.CharField(max_length=8)
    logradouro = peewee.CharField()
    numero = peewee.CharField()
    bairro = peewee.CharField()
    complemento = peewee.CharField()
    cidade = peewee.CharField()
    estado = peewee.CharField()

    @classmethod
    def criar(cls, dados):
        if len(dados['senha']) < 6:
          raise werkzeug.exceptions.BadRequest(f'A senha deve ter no mínimo 6 caracteres')

        if cls.select().where(cls.cpf == dados['cpf']).exists():
          raise werkzeug.exceptions.BadRequest(f'Já existe um usuário com o CPF')
        
        hashed_password = bcrypt.hashpw(dados['senha'].encode('utf-8'), bcrypt.gensalt())
        dados['senha'] = hashed_password.decode('utf-8')

        novo_usuario = cls.create(**dados)
        return novo_usuario
        
    @classmethod
    def buscar_por_cpf(cls, user_cpf):
        try:
            usuario = cls.get(cls.cpf == user_cpf)
            return usuario
        
        except DoesNotExist:
          raise werkzeug.exceptions.NotFound(f'Usuário não encontrado')


    @classmethod
    def alterar(cls, user_cpf, dados):
      try:
          usuario = Usuario.get(Usuario.cpf == user_cpf)

          if 'whatsapp' in dados:
              usuario.whatsapp = dados['whatsapp']
          if 'cep' in dados:
              usuario.cep = dados['cep']
          if 'logradouro' in dados:
              usuario.logradouro = dados['logradouro']
          if 'numero' in dados:
              usuario.numero = dados['numero']
          if 'bairro' in dados:
              usuario.bairro = dados['bairro']
          if 'complemento' in dados:
              usuario.complemento = dados['complemento']
          if 'cidade' in dados:
              usuario.cidade = dados['cidade']
          if 'estado' in dados:
              usuario.estado = dados['estado']

          usuario.save()
          return usuario
      
      except DoesNotExist:
          raise werkzeug.exceptions.NotFound(f'Usuário com ID {user_cpf} não encontrado.')

        
    @classmethod
    def listar(cls, cpf):
        usuario_entity = cls.buscar_por_cpf(cpf)

        if usuario_entity:
            print('Usuário encontrado:')
            print(f'Nome: {usuario_entity.nome} {usuario_entity.sobrenome}')
            print(f'Email: {usuario_entity.email}')
            print(f'Whatsapp: {usuario_entity.whatsapp}')
            print(f'CEP: {usuario_entity.cep}')
            print(f'Logradouro: {usuario_entity.logradouro}')
            print(f'Número: {usuario_entity.numero}')
            print(f'Bairro: {usuario_entity.bairro}')
            print(f'Cidade: {usuario_entity.cidade}')
            print(f'Estado: {usuario_entity.estado}')
        else:
            raise werkzeug.exceptions.NotFound('Usuário não encontrado')

    @classmethod
    def deletar(cls, user_cpf):
        try:
            usuario = cls.get(cls.cpf == user_cpf)
            usuario.delete_instance()
            print(f"Usuário com ID {user_cpf} deletado com sucesso.")
        
        except DoesNotExist:
          raise werkzeug.exceptions.BadRequest(f'Usuário {user_cpf} não encontrado.')

