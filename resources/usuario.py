from ast import arguments
from flask_restful import Resource, reqparse

usuarios = [
    {
        'usuario_id': 1,
        'nome': 'Matheus',
        'sobrenome': 'Orozimbo',
        'email': 'matheus@matheus.com',
        'senha': '123456789',
        'telefone': '123',
        'CPF': 'uiujkljkj',
        'CEP': '1235567',
        'Cidade': 'jhjhjhf',
        'logradouro': 'jhaajH',
        'rua': 'sjhajhfahf',
        'número': 12
    },
    {
        'usuario_id': 2,
        'nome': 'Matheus',
        'sobrenome': 'Orozimbo',
        'email': 'matheus@matheus.com',
        'senha': '123456789',
        'telefone': '123',
        'CPF': 'uiujkljkj',
        'CEP': '1235567',
        'cidade': 'jhjhjhf',
        'logradouro': 'jhaajH',
        'rua': 'sjhajhfahf',
        'número': 12
    },
]

class Usuarios(Resource):

    def get(self):
        return {'usuarios': usuarios}

class Usuario(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('sobrenome')
    argumentos.add_argument('email')
    argumentos.add_argument('senha')
    argumentos.add_argument('telefone')
    argumentos.add_argument('CPF')
    argumentos.add_argument('CEP')
    argumentos.add_argument('cidade')
    argumentos.add_argument('logradouro')
    argumentos.add_argument('rua')
    argumentos.add_argument('numero')

    def buscar_usuario(usuario_id):
        for usuario in usuarios:
            if usuario['usuario_id'] == usuario_id:
                return usuario
        return None

    def get(self, usuario_id):
        
        usuario = Usuario.buscar_usuario(usuario_id)
        if usuario:
            return usuario
        return {'mensagem': 'Usuário  não encontrado.'}, 404

    def post(self, usuario_id):

        dados = Usuario.argumentos.parse_args()
        novo_usuario = { 'usuario_id': usuario_id, **dados }

        usuarios.append(novo_usuario)
        return novo_usuario, 201

    def put(self, usuario_id):
        
        dados = Usuario.argumentos.parse_args()
        novo_usuario = { 'usuario_id': usuario_id, **dados }

        usuario = Usuario.buscar_usuario(usuario_id)
        if usuario:
            usuario.update(novo_usuario)
            return novo_usuario, 200

        usuarios.append(novo_usuario)
        return novo_usuario, 201

    def delete(self, usuario_id):
        pass