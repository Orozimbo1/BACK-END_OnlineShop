from flask_restful import Resource, reqparse

from models.usuario import UsuarioModel

class Usuarios(Resource):

    def get(self):
        return UsuarioModel(usuarios)

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

    def get(self, usuario_id):
        
        usuario = UsuarioModel.buscar_usuario(usuario_id)
        if usuario:
            return usuario.json()
        return {'mensagem': 'Usuário  não encontrado.'}, 404

    def post(self, usuario_id):

        if UsuarioModel.buscar_usuario(usuario_id):
            return {"mensagem": "Usuário já cadastrado"}, 404

        dados = Usuario.argumentos.parse_args()
        usuario = UsuarioModel(usuario_id, **dados)
        usuario.salvar_usuario()

        return usuario.json(), 201

    def put(self, usuario_id):
        
        dados = Usuario.argumentos.parse_args()

        usuario_encontrado = UsuarioModel.buscar_usuario(usuario_id)
        if usuario_encontrado:
            usuario_encontrado.atualizar_usuario(**dados)
            usuario_encontrado.salvar_usuario()
            return usuario_encontrado.json(), 200

        usuario = UsuarioModel(usuario_id, **dados)
        usuario.salvar_usuario()
        return usuario.json(), 201

    def delete(self, usuario_id):
        usuario = UsuarioModel.buscar_usuario(usuario_id)

        if usuario:
            usuario.deletar_usuario()
            return {"mensagem":"Usuário deletado com sucesso"}, 200
        return {'mensagem': 'Usuário não encontrado.'}, 404