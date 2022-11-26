from datetime import  timedelta
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash
from blacklist import BLACKLIST
from models.usuario import UsuarioModel


argumentos = reqparse.RequestParser()
argumentos.add_argument('img_perfil_usuario', type=str)
argumentos.add_argument('nome', type=str, required=True, help="O campo 'nome' não pode ser deixado em branco.")
argumentos.add_argument('sobrenome', type=str, required=True, help="O campo 'sobrenome' não pode ser deixado em branco.")
argumentos.add_argument('email', type=str, required=True, help="O campo 'email' não pode ser deixado em branco.")
argumentos.add_argument('senha', type=str, required=True, help="O campo 'senha' não pode ser deixado em branco.")
argumentos.add_argument('CPF', type=str)
argumentos.add_argument('contato_usuario_id', type=int)
argumentos.add_argument('endereco_usuario_id', type=int)

class Usuarios(Resource):

    def get(self):
        usuarios = UsuarioModel.buscar_todos_usuarios()
        return usuarios 

class Usuario(Resource):

    def get(self, usuario_id):
        
        usuario = UsuarioModel.buscar_usuario(usuario_id)
        if usuario:
            return usuario.json()
        return {'mensagem': 'Usuário  não encontrado.'}, 404

    # @jwt_required()
    def put(self, usuario_id):
        
        atributos = reqparse.RequestParser()
        atributos.add_argument('nome', type=str)
        atributos.add_argument('sobrenome', type=str)
        atributos.add_argument('email', type=str)
        atributos.add_argument('CPF', type=str)
        atributos.add_argument('contato_usuario_id', type=int)
        atributos.add_argument('endereco_usuario_id', type=int)
        data = atributos.parse_args()

        usuario_encontrado = UsuarioModel.buscar_usuario(usuario_id)
        if usuario_encontrado:
            try:
                usuario_encontrado.atualizar_usuario(**data)
                print("aooba")
                usuario_encontrado.salvar_usuario()
            except:
                return {'mensagem': 'Houve um erro tentando atualizar o usuário.'}, 500
            return usuario_encontrado.json(), 200

    # @jwt_required()
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

        dados = argumentos.parse_args()
        hash = generate_password_hash(dados['senha'])
        

        if UsuarioModel.buscar_email_usuario(dados['email']):
            return {"mensagem": "Email '{}' já cadastrado".format(dados['email'])}, 404

        usuario = UsuarioModel(**dados)
        try:
            usuario.hash_senha(dados['senha'])
            usuario.salvar_usuario()
            expires = timedelta(days=10)
            token_de_acesso = create_access_token(identity=usuario.usuario_id, expires_delta=expires)
        except Exception as e:
            print(str(e))
            return {'mensagem': 'Houve um erro tentando salvar o usuário.'}, 500
        return (token_de_acesso, usuario.json()), 201

class UsuarioLogin(Resource):
    
    @classmethod
    def post(cls):
        atributos = reqparse.RequestParser()
        atributos.add_argument('email', type=str, required=True, help="O campo 'email' não pode ser deixado em branco.")
        atributos.add_argument('senha', type=str, required=True, help="O campo 'senha' não pode ser deixado em branco.")
        dados = atributos.parse_args()

        usuario = UsuarioModel.buscar_email_usuario(dados['email'])

        if usuario and safe_str_cmp and check_password_hash(usuario.senha, dados['senha']):
            expires = timedelta(days=10)
            token_de_acesso = create_access_token(identity=usuario.usuario_id, expires_delta=expires)
            return (token_de_acesso, usuario.json()), 200
        return {'mensagem': 'Usuário ou senha incorreto.'}, 401

class UsuarioLogout(Resource):
    
    # @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logout com sucesso.'}, 200