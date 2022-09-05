from enum import unique
from os import access
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp

from models.usuario import UsuarioModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('nome', type=str, required=True, help="O campo 'nome' não pode ser deixado em branco.")
argumentos.add_argument('sobrenome', type=str, required=True, help="O campo 'sobrenome' não pode ser deixado em branco.")
argumentos.add_argument('email', type=str, required=True, help="O campo 'email' não pode ser deixado em branco.")
argumentos.add_argument('senha', type=str, required=True, help="O campo 'senha' não pode ser deixado em branco.")
argumentos.add_argument('telefone', type=str)
argumentos.add_argument('CPF', type=str)
argumentos.add_argument('CEP', type=str)
argumentos.add_argument('cidade', type=str)
argumentos.add_argument('logradouro', type=str)
argumentos.add_argument('rua', type=str)
argumentos.add_argument('numero', type=int)

class Usuarios(Resource):

    def get(self):
        return {'usuarios': [usuario.json() for usuario in UsuarioModel.query.all()]}

class Usuario(Resource):

    def get(self, usuario_id):
        
        usuario = UsuarioModel.buscar_usuario(usuario_id)
        if usuario:
            return usuario.json()
        return {'mensagem': 'Usuário  não encontrado.'}, 404

    def put(self, usuario_id):
        
        dados = argumentos.parse_args()

        usuario_encontrado = UsuarioModel.buscar_usuario(usuario_id)
        if usuario_encontrado:
            usuario_encontrado.atualizar_usuario(**dados)
            usuario_encontrado.salvar_usuario()
            return usuario_encontrado.json(), 200

        usuario = UsuarioModel(usuario_id, **dados)
        try:
            usuario.salvar_usuario()
        except:
            return {'mensagem': 'Houve um erro tentando salvar o usuário.'}, 500
        return usuario.json(), 201

    def delete(self, usuario_id):
        usuario = UsuarioModel.buscar_usuario(usuario_id)

        if usuario:
            try:
                usuario.deletar_usuario()
            except:
                return {'mensagem': 'Houve um erro tentando deletar o usuário.'}, 500
            return {"mensagem":"Usuário deletado com sucesso"}, 200
        return {'mensagem': 'Usuário não encontrado.'}, 404

class UsuarioCadastro(Resource):

    def post(self):

        dados =argumentos.parse_args()

        if UsuarioModel.buscar_email_usuario(dados['email']):
            return {"mensagem": "Email '{}' já cadastrado".format(dados['email'])}, 404

        usuario = UsuarioModel(**dados)
        try:
            usuario.salvar_usuario()
        except:
            return {'mensagem': 'Houve um erro tentando salvar o usuário.'}, 500
        return {"mensagem": "Usuário '{}' criado com sucesso.".format(dados['nome'] + ' ' + dados['sobrenome'])}, 201

class UsuarioLogin(Resource):
    
    @classmethod
    def post(cls):
        atributos = reqparse.RequestParser()
        atributos.add_argument('email', type=str, required=True, help="O campo 'email' não pode ser deixado em branco.")
        atributos.add_argument('senha', type=str, required=True, help="O campo 'senha' não pode ser deixado em branco.")
        dados = atributos.parse_args()

        usuario = UsuarioModel.buscar_email_usuario(dados['email'])

        if usuario and safe_str_cmp(usuario.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=usuario.usuario_id)
            return {'token de acesso': token_de_acesso}, 200
        return {'mensagem': 'Usuário ou senha incorreto.'}, 401