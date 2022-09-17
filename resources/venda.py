from flask_restful import Resource, reqparse
from models.venda import VendaModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('produto_id', type=int,required= True, help= " O campo 'produto' precisa ser preenchido.")


class Vendas(Resource):

    def get(self):

        produtos = VendaModel.buscar_todas_vendas()
        return produtos

class Venda(Resource):

    def get(self, venda_id):
        
        venda = VendaModel.buscar_produtos(venda_id)
        if venda:
            return venda.json()
        return {'mensagem': 'Venda não encontrado.'}, 404

    def delete(self, venda_id):
        venda = VendaModel.buscar_vendas(venda_id)
        if venda:
            try:
                venda.deletar_produto()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "venda deletado com sucesso"}
        return{"mensagem":"Produto não encontrado"}

class VendaCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()
        venda = VendaModel(**dados)
        venda.salvar_venda()
        try:
            venda.salvar_venda()
        except:
            return {"mensagem":"Ocorreu um erro interno"}, 500
        return venda.json()