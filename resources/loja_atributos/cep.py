from flask_restful import Resource, reqparse
from models.loja_atributos.cep import CepLojaModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('CEP', type=str)
argumentos.add_argument('UF', type=str)
argumentos.add_argument('cidade', type=str)
argumentos.add_argument('bairro', type=str)
argumentos.add_argument('rua', type=str)
argumentos.add_argument('numero', type=int)

class CepLojas(Resource):

    def get(self):
        enderecos = CepLojaModel.buscar_todos_enderecos()
        return enderecos

class CepLoja(Resource):

    def get(self, endereco_loja_id):
        
        endereco = CepLojaModel.buscar_endereco_por_id(endereco_loja_id)
        if endereco:
            return endereco.json()
        return {'mensagem': 'Endereco não encontrado.'}, 404

    def put(self, endereco_loja_id):
        
        dados = argumentos.parse_args()

        endereco = CepLojaModel.buscar_endereco_por_id(endereco_loja_id)
        if endereco:
            endereco.atualizar_endereco(**dados)
            endereco.salvar_loja()
            return endereco.json(), 200
        endereco =CepLojaModel(endereco_loja_id, **dados )

        try:
            endereco.salvar_loja()
        except:
            return {"Ocorreu um erro interno"}, 500
        return endereco.json(), 201

    def delete(self, endereco_loja_id):
        endereco = CepLojaModel.buscar_endereco_por_id(endereco_loja_id)
        if endereco:
            try:
                endereco.deletar_loja()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "Endereço deletado com sucesso"}
        return{"mensagem":"Endereço não encontrado"}

class CepLojaCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()

        endereco = CepLojaModel(**dados)
        try:
            endereco.salvar_endereco()
        except:
            return {'mensagem': 'Houve um erro tentando salvar o endereço.'}, 500
        return endereco.json()