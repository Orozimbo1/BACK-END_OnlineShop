from flask_restful import Resource, reqparse
from models.loja import LojaModel
from models.produto import ProdutoModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('genero_produto_id', type=str)
argumentos.add_argument('secao_produto_id', type=str)
argumentos.add_argument('categoria_produto_id', type=str)
argumentos.add_argument('estilo_produto_id', type=str)
argumentos.add_argument('nome', type=str)
argumentos.add_argument('descricao', type=str)
argumentos.add_argument('cor_produto', type=str)
argumentos.add_argument('tamanho_produto', type=str)
argumentos.add_argument('qtd_estoque', type=int)
argumentos.add_argument('valor', type=float)
argumentos.add_argument('loja_id', type=int)

class Produtos(Resource):

    def get(self):

        produtos = ProdutoModel.buscar_todos_produtos()
        return produtos

class Produto(Resource):

    def get(self, produto_id):
        
        produto = ProdutoModel.buscar_produtos(produto_id)
        if produto:
            return produto.json()
        return {'mensagem': 'Produto não encontrado.'}, 404

    def put(self, produto_id):
        
        dados = argumentos.parse_args()

        produto_encontrado = ProdutoModel.buscar_produtos(produto_id)
        if produto_encontrado:
            produto_encontrado.atualizar_produto(**dados)
            produto_encontrado.salvar_produto()
            return produto_encontrado.json(), 200

        produto = ProdutoModel( produto_id, **dados )

        try:
            produto.salvar_produto()
        except:
            return {"Ocorreu um erro interno"}, 500
        return produto.json(), 201

    def delete(self, produto_id):
        produto = ProdutoModel.buscar_produtos(produto_id)
        if produto:
            try:
                produto.deletar_produto()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "Produto deletado com sucesso"}, 200
        return{"mensagem":"Produto não encontrado"},404

class ProdutoCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()
        produto = ProdutoModel(**dados)
        loja = LojaModel.buscar_loja_por_id(dados.get('loja_id'))
        if loja:
            try:
                produto.salvar_produto()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return produto.json()
        return {"mensagem": "Essa loja não existe. Por favor insira um 'id' válido."}

class ProdutoFiltro(Resource):
    def get(self, genero_produto_id):

        produtos = ProdutoModel.buscar_produtos_filtro(genero_produto_id)
        return produtos