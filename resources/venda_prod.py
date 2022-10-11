from math import prod
from flask_restful import Resource, reqparse
from models.produto import ProdutoModel
from models.venda_prod import VendaProdModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('produto_id', type=int, required=True, help= "O campo 'produto_id' precisa ser preenchido.")
argumentos.add_argument('qtd_produtos', type=int)
argumentos.add_argument('total', type=int)
argumentos.add_argument('venda_id', type=int)


class VendasProd(Resource):

    def get(self):

        vendas_prod = VendaProdModel.buscar_todas_vendas_prod()
        return vendas_prod

class VendaProd(Resource):

    def get(self, venda_prod_id):
        
        venda_prod = VendaProdModel.buscar_venda_prod(venda_prod_id)
        if venda_prod:
            return venda_prod.json()
        return {'mensagem': 'A venda do produto não foi encontrada.'}, 404


    def delete(self, venda_prod_id):
        venda_prod = VendaProdModel.buscar_venda_prod(venda_prod_id)
        if venda_prod:
            try:
                venda_prod.deletar_venda_prod()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "A venda do produto foi deletada com sucesso"}
        return{"mensagem":"A venda do produto não foi encontrada."}

class VendaProdCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()
        venda_prod = VendaProdModel(**dados)
        produto = ProdutoModel.buscar_produtos(dados.get('produto_id'))
        if produto:
            qtd_estoque = produto.qtd_estoque - dados.get('qtd_produtos')
            try:
                print(produto.json())
                if qtd_estoque >=0:
                    produto.atualizar_qtd_produto(qtd_estoque)
                    venda_prod.salvar_venda_prod()
                    return venda_prod.json()
                return {"mensagem": "Quantidade inválida, só existem '{}' produtos no estoque".format(produto.qtd_estoque)}
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
        return {"mensagem": "Esse produto não existe. Por favor insira um 'id' válido."}