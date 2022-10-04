from flask_restful import Resource, reqparse
from models.produto_atributos.qtd_estoque import QtdProdutoModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('qtd_produto', type=str, required=True, help= "O campo 'qtd_produto' precisa ser preenchido.")


class QtdProdutos(Resource):

    def get(self):

        qtd_produtos = QtdProdutoModel.buscar_todas_qtds()
        return qtd_produtos

class QtdProduto(Resource):

    def get(self, qtd_estoque_id):
        
        qtd_produto = QtdProdutoModel.buscar_qtd(qtd_estoque_id)
        if qtd_produto:
            return qtd_produto.json()
        return {'mensagem': 'A quantidade de produto não foi encontrada.'}, 404

    def put(self, qtd_estoque_id):
        
        dados = argumentos.parse_args()

        qtd_produto_encontrada = QtdProdutoModel.buscar_qtd(qtd_estoque_id)

        if qtd_produto_encontrada:
            qtd_produto_encontrada.atualizar_qtd(**dados)
            qtd_produto_encontrada.salvar_qtd()
            return qtd_produto_encontrada.json(), 200

        qtd_produto = QtdProdutoModel( qtd_estoque_id, **dados )

        try:
            qtd_produto.salvar_qtd()
        except:
            return {"Ocorreu um erro interno"}, 500
        return qtd_produto.json(), 201

    def delete(self, qtd_estoque_id):
        qtd_produto = QtdProdutoModel.buscar_qtd(qtd_estoque_id)
        if qtd_produto:
            try:
                qtd_produto.deletar_qtd()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "A quantidade do produto foi deletada com sucesso"}
        return{"mensagem":"A quantidade do produto não foi encontrada."}

class QtdProdutoCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()
        qtd_produto = QtdProdutoModel(**dados)
        try:
            qtd_produto.salvar_qtd()
        except:
            return {"mensagem":"Ocorreu um erro interno"}, 500
        return qtd_produto.json()