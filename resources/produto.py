from flask_restful import Resource, reqparse
from models.loja import LojaModel
from models.produto import ProdutoModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('genero_produto_id', type=str, help= " O campo 'Gênero' precisa ser preenchido.")
argumentos.add_argument('secao_produto_id', type=str, help= " O campo 'Seção' precisa ser preenchido.")
argumentos.add_argument('categoria_produto_id', type=str, help= " O campo 'Categoria' precisa ser preenchido.")
argumentos.add_argument('estilo_produto_id', type=str, help= " O campo 'Estilo' precisa ser preenchido.")
argumentos.add_argument('nome', type=str, help= " O campo 'Nome' precisa ser preenchido.")
argumentos.add_argument('descricao', type=str)
argumentos.add_argument('cor_produto', type=str, help= " O campo 'Cor' precisa ser preenchido.")
argumentos.add_argument('tamanho_produto', type=str, help= " O campo 'Tamanho' precisa ser preenchido.")
argumentos.add_argument('qtd_estoque', type=int, help= " O campo 'Quantidade em estoque' precisa ser preenchido.")
argumentos.add_argument('valor', type=float, help= " O campo 'Valor' precisa ser preenchido.")
argumentos.add_argument('loja_id', type=int, help= " O produto tem que estar associado à alguma loja.")

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
            return{"mensagem": "Produto deletado com sucesso"}
        return{"mensagem":"Produto não encontrado"}

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