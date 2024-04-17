from datetime import date
from models.user import Usuario
from models.login import Autenticacao
from models.interdicoes import Interdicoes

# Usuario.create_table()

Interdicoes.create_table()
# Interdicoes.drop_table()

dados_usuario = {
  'nome': 'John',
  'sobrenome': 'Doe',
  'cpf': '01234567899',
  'whatsapp': '99999999999',
  'email': 'johndoe@email.com',
  'senha': 'senha1',
  'cep': '99999999',
  'logradouro': 'R. Número Zero',
  'numero': '00',
  'bairro': 'Zero',
  'complemento': 'Casa 0',
  'cidade': 'Cidade zero',
  'estado': 'ZE'
}

# # Insere dados na tabela usuários
novo_usuario = Usuario.criar(dados_usuario)

# # listar usuário por CPF
# Usuario.listar('01234567899')

# dados_para_atualizar = {
#   'whatsapp': '987654321',
#   'cep': '12345678',
#   'logradouro': 'Nova Rua',
#   'numero': '100',
#   'bairro': 'Novo Bairro',
#   'complemento': 'Apto 101',
#   'cidade': 'Nova Cidade',
#   'estado': 'SP'
# }

# # alterar dados do usuario
# Usuario.alterar('01234567899', dados_para_atualizar)
# Usuario.listar('01234567899')

# Usuario.deletar('01234567899')  # CPF do usuário a ser deletado


# # Testa metodo de autenticação
cpf = '01234567899'
senha = 'senha1'
usuario_autenticado = Autenticacao.login(cpf, senha)

if usuario_autenticado:
  print(f'Login realizado')
  print(f'Nome: {usuario_autenticado.nome} {usuario_autenticado.sobrenome}')
  print(f'Email: {usuario_autenticado.email}')

  nova_interdicao = Interdicoes.criar(
  tipo = 'Obras',
  cep = '12345678',
  logradouro = 'Rua das Obras',
  numero = '123',
  bairro = 'Centro',
  cidade = 'São Paulo',
  estado = 'SP',
  data = date.today(), 
  descricao = 'Via alagada',
  usuario = usuario_autenticado.id
)

  if nova_interdicao:
    print('Interdição criada com sucesso!')
  else:
    print('Erro ao criar interdição. Verifique os campos obrigatórios.')

else:
  print('Não foi possivel se conectar.')

# Buscar
interdicoes_obras = Interdicoes.buscar_por_tipo('Alagamentos')
if interdicoes_obras:
    print(f'Interdições do tipo "Alagamentos":')
    for interdicao in interdicoes_obras:
        print(f'ID: {interdicao.id}, Tipo: {interdicao.tipo}')
else:
    print('Não foram encontradas interdições do tipo "Alagamentos".')

# Listar
todas_interdicoes = Interdicoes.listar()
if todas_interdicoes:
    print('Todas as interdições:')
    for interdicao in todas_interdicoes:
        print(f'ID: {interdicao.id}, Tipo: {interdicao.tipo}')
else:
    print('Não foram encontradas interdições.')

# Deletar
# interdicao_id = '1d925933-6690-4667-bfa7-9addc61b5bad'
# Interdicoes.deletar(interdicao_id)