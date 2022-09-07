from flask_restful import Resource, reqparse
from models.loja import LojaModel


class Lojas(Resource):

    def get(self):
        return {"Lojas": [loja.json() for loja in LojaModel.query.all()]}

class Loja(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome_fantasia', type=str,required= True, help= " O campo 'Nome Fantasia' precisa ser preenchido")
    argumentos.add_argument('email', type=str,required=True, help= "O campo 'e-mail' precisa ser preenchido")
    argumentos.add_argument('senha', type=str, required=True, help= "O campo 'senha' precisa ser preenchido]")
    argumentos.add_argument('CNPJ', type=str,required= True, help= " O campo 'Seção' precisa ser preenchido")
    argumentos.add_argument('telefone', type=str,required= True, help= " O campo 'Telefone' precisa ser preenchido")
    argumentos.add_argument('CEP', type=str,required= True, help= " O campo 'CEP' precisa ser preenchido")
    argumentos.add_argument('cidade', type=str,required= True, help= " O campo 'Cidade' precisa ser preenchido")
    argumentos.add_argument('logradouro', type=str,required= True, help= " O campo 'Logradouro' precisa ser preenchido")
    argumentos.add_argument('rua', type=str,required= True, help= " O campo 'Rua' precisa ser preenchido")
    argumentos.add_argument('numero', type=int,required= True, help= " O campo 'Número' precisa ser preenchido")

    def get(self, nome_fantasia):
        
        loja = LojaModel.buscar_lojas(nome_fantasia)
        if loja:
            return loja.json()
        return {'mensagem': 'Loja não encontrada.'}, 404

    def put(self, loja_id):
        
        dados = Loja.argumentos.parse_args()

        loja_encontrada = LojaModel.buscar_lojas(loja_id)
        if loja_encontrada:
            loja_encontrada.atualizar_loja(**dados)
            loja_encontrada.salvar_loja()
            return loja_encontrada.json(), 200
        loja =LojaModel(loja_id, **dados )

        try:
            loja.salvar_loja()
        except:
            return {"Ocorreu um erro interno"}, 500
        return loja.json(), 201

    def delete(self, loja_id):
        loja = LojaModel.buscar_lojas(loja_id)
        if loja:
            try:
                loja.deletar_loja()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "Loja deletada com sucesso"}
        return{"mensagem":"Loja não encontrada"}

class LojaCadastro(Resource):

    def post(self):

        dados = Loja.argumentos.parse_args()

        if LojaModel.buscar_lojas(dados['nome_fantasia']):
            return {"mensagem":"Loja '{}' já existente !".format(dados['nome_fantasia'])}, 404

        loja = LojaModel(**dados)
        try:
            loja.salvar_loja()
        except:
            return {"mensagem":"Ocorreu um erro interno"}, 500
        return loja.json()
