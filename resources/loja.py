from flask_restful import Resource, reqparse
from models.loja import LojaModel
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from blacklist import BLACKLIST



argumentos = reqparse.RequestParser()
argumentos.add_argument('nome_fantasia', type=str, required=True, help= " O campo 'Nome Fantasia' precisa ser preenchido")
argumentos.add_argument('email', type=str, required=True, help= "O campo 'e-mail' precisa ser preenchido")
argumentos.add_argument('senha', type=str, required=True, help= "O campo 'senha' precisa ser preenchido]")
argumentos.add_argument('CNPJ', type=str, required=True, help= " O campo 'Seção' precisa ser preenchido")
argumentos.add_argument('contato_loja_id', type=int)
argumentos.add_argument('endereco_loja_id', type=int)

class Lojas(Resource):

    def get(self):
        lojas = LojaModel.buscar_todas_lojas()
        return lojas

class Loja(Resource):

    def get(self, nome_fantasia):
        
        loja = LojaModel.buscar_lojas(nome_fantasia)
        if loja:
            return loja.json()
        return {'mensagem': 'Loja não encontrada.'}, 404

    def put(self, nome_fantasia):
        
        dados = argumentos.parse_args()

        loja_encontrada = LojaModel.buscar_lojas(nome_fantasia)
        if loja_encontrada:
            loja_encontrada.atualizar_loja(**dados)
            loja_encontrada.salvar_loja()
            return loja_encontrada.json(), 200
        loja =LojaModel(nome_fantasia, **dados )

        try:
            loja.salvar_loja()
        except:
            return {"Ocorreu um erro interno"}, 500
        return loja.json(), 201

    def delete(self, nome_fantasia):
        loja = LojaModel.buscar_lojas(nome_fantasia)
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

        if LojaModel.buscar_lojas(dados['nome_fantasia']):
            return {"mensagem":"Loja '{}' já existente !".format(dados['nome_fantasia'])}, 404

        loja = LojaModel(**dados)
        try:
            loja.hash_senha_loja(dados['senha'])
            loja.salvar_loja()
        except Exception as e:
            print(str(e))
            return {'mensagem': 'Houve um erro tentando salvar loja.'}, 500
        return loja.json()

class LojaLogin(Resource):
    
    @classmethod
    def post(cls):
        atributos = reqparse.RequestParser()
        atributos.add_argument('email', type=str, required=True, help="O campo 'email' não pode ser deixado em branco.")
        atributos.add_argument('senha', type=str, required=True, help="O campo 'senha' não pode ser deixado em branco.")
        dados = atributos.parse_args()

        loja = LojaModel.buscar_loja_por_email(dados['email'])

        if loja and safe_str_cmp and check_password_hash(loja.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=loja.loja_id)
            return {'token de acesso': token_de_acesso}, 200
        return {'mensagem': 'Usuário ou senha incorreto.'}, 401

class LojaLogout(Resource):
    
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logout com sucesso.'}, 200
