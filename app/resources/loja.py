from datetime import  timedelta
from flask_restful import Resource, reqparse
from models.loja import LojaModel
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from blacklist import BLACKLIST



argumentos = reqparse.RequestParser()
argumentos.add_argument('img_perfil_loja', type=str)
argumentos.add_argument('nome_fantasia', type=str, required=True, help= " O campo 'Nome Fantasia' precisa ser preenchido")
argumentos.add_argument('email', type=str, required=True, help= "O campo 'e-mail' precisa ser preenchido")
argumentos.add_argument('senha', type=str, required=True, help= "O campo 'senha' precisa ser preenchido]")
argumentos.add_argument('CNPJ', type=str, required=True, help= " O campo 'Seção' precisa ser preenchido")

class Lojas(Resource):

    def get(self):
        lojas = LojaModel.buscar_todas_lojas()
        return lojas

class Loja(Resource):

    def get(self, loja_id):
        
        loja = LojaModel.buscar_loja_por_id(loja_id)
        if loja:
            return loja.json()
        return {'mensagem': 'Loja não encontrada.'}, 404

    def put(self, loja_id):
        atributos = reqparse.RequestParser()
        atributos.add_argument('img_perfil_loja', type=str)
        atributos.add_argument('nome_fantasia', type=str)
        atributos.add_argument('email', type=str)
        atributos.add_argument('CNPJ', type=str)
        
        data = atributos.parse_args()

        loja_encontrada = LojaModel.buscar_loja_por_id(loja_id)
        if loja_encontrada:
            try:
                loja_encontrada.atualizar_loja(**data)
                loja_encontrada.salvar_loja()
            except:
                return {"Ocorreu um erro interno"}, 500
            return loja_encontrada.json(), 200

    def delete(self, loja_id):
        loja = LojaModel.buscar_loja_por_id(loja_id)
        if loja:
            try:
                loja.deletar_loja()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "Loja deletada com sucesso"}
        return{"mensagem":"Loja não encontrada"}

class LojaCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()
        hash = generate_password_hash(dados['senha'])

        if LojaModel.buscar_loja_por_email(dados['email']):
            return {"mensagem":"Loja '{}' já existente !".format(dados['email'])}, 401

        loja = LojaModel(**dados)
        try:
            loja.hash_senha_loja(dados['senha'])
            loja.salvar_loja()
            expires = timedelta(days=10)
            token_de_acesso = create_access_token(identity=loja.loja_id, expires_delta= expires)
        except Exception as e:
            print(str(e))
            return {'mensagem': 'Houve um erro tentando salvar loja.'}, 500
        return  (token_de_acesso, loja.json()), 201

class LojaLogin(Resource):
    
    @classmethod
    def post(cls):
        atributos = reqparse.RequestParser()
        atributos.add_argument('email', type=str, required=True, help="O campo 'email' não pode ser deixado em branco.")
        atributos.add_argument('senha', type=str, required=True, help="O campo 'senha' não pode ser deixado em branco.")
        dados = atributos.parse_args()

        loja = LojaModel.buscar_loja_por_email(dados['email'])
        print("##########################")
        print(dados['senha'])
        print("##########################")
        if loja and safe_str_cmp and check_password_hash(loja.senha, dados['senha']):
            expires = timedelta(days=10)
            token_de_acesso = create_access_token(identity=loja.loja_id, expires_delta= expires)
            return  (token_de_acesso, loja.json()), 200
        return {'mensagem': 'Credenciais incorretas.'}, 401

class LojaLogout(Resource):
    
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logout com sucesso.'}, 200
