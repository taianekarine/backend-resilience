import bcrypt
from models.user import Usuario

class Autenticacao:
  @staticmethod
  def login(cpf, senha):
    try:
      usuario = Usuario.get(Usuario.cpf == cpf)

      if bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
          return usuario 
      
      else:
          return None
    
    except Usuario.DoesNotExist:
      return 'Usuário não existe'
