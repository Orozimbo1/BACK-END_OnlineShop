from flask_restful import Resource, reqparse
from models.produto import ProdutoModel


class Produtos(Resource):

    def get(self):
        return ProdutoModel(produtos)

class Produto(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('genero')
    argumentos.add_argument('secao')
    argumentos.add_argument('categoria')
    argumentos.add_argument('estilo')
    argumentos.add_argument('nome')
    argumentos.add_argument('descricao')
    argumentos.add_argument('qtd_estoque')
    argumentos.add_argument('cor')
    argumentos.add_argument('tamanho')
    argumentos.add_argument('preco')

    def get(self, produto_id):
        
        produto = ProdutoModel.buscar_produtos(produto_id)
        if produto:
            return produto.json()
        return {'mensagem': 'Produto não encontrado.'}, 404

    def post(self, produto_id):

        if ProdutoModel.buscar_produtos(produto_id):
            return {"mensagem":"Produto com o id'{}'  já existe!"}, 404

        dados = Produto.argumentos.parse_args()
        produto = ProdutoModel(produto_id, **dados)
        produto.salvar_produto()
        return produto.json()

    def put(self, produto_id):
        
        dados = Produto.argumentos.parse_args()

        produto_encontrado = ProdutoModel.buscar_produtos(produto_id)
        if produto_encontrado:
            produto_encontrado.atualizar_produto(**dados)
            produto_encontrado.salvar_produto()
            return produto_encontrado.json(), 200
        produto = { 'produto_id': produto_id, **dados }

        produto.salvar_produto()
        return produto.json(), 201

    def delete(self, produto_id):
        produto = ProdutoModel.buscar_produtos(produto_id)
        if produto:
            produto.deletar_produto()
            return {"mensagem":"Produto deletado com sucesso"}, 200
        return{"mensagem":"Produto não encontrado"}