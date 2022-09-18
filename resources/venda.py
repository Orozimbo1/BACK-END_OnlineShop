from flask_restful import Resource, reqparse
from models.loja import LojaModel
from models.venda import VendaModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('loja_id', type=int,required= True, help= " O campo 'produto' precisa ser preenchido.")
argumentos.add_argument('produto_id', type=int,required= True, help= " O campo 'produto' precisa ser preenchido.")
# argumentos.add_argument('usuario_id', type=int,required= True, help= " O campo 'usuario' precisa ser preenchido.")


class Vendas(Resource):

    def get(self):

        vendas = VendaModel.buscar_todas_vendas()
        return vendas

class Venda(Resource):

    def get(self, venda_id):
        
        venda = VendaModel.buscar_vendas(venda_id)
        if venda:
            return venda.json()
        return {'mensagem': 'Venda não encontrado.'}, 404

    def delete(self, venda_id):
        venda = VendaModel.buscar_vendas(venda_id)
        if venda:
            try:
                venda.deletar_venda()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "Venda deletada com sucesso"}
        return{"mensagem":"Venda não encontrada"}

class VendaCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()
        venda = VendaModel(**dados)
        loja = LojaModel.buscar_loja_por_id(dados.get('loja_id'))
        if loja:
            try:
                venda.salvar_venda()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return venda.json()
        return {"mensagem":"A loja não foi encontrada"}, 500