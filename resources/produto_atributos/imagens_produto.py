from flask_restful import Resource, reqparse
from models.produto_atributos.imagens_produto import ImagemProdutoModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('url_imagem', type=str, required=True, help= "O campo 'nome_imagens_produto' precisa ser preenchido.")
argumentos.add_argument('descricao_imagem', type=str, required=True, help= "O campo 'nome_imagens_produto' precisa ser preenchido.")


class ImagensProdutos(Resource):

    def get(self):

        imagens_produtos = ImagemProdutoModel.buscar_todas_imagens()
        return imagens_produtos

class ImagemProduto(Resource):

    def get(self, imagem_produto_id):
        
        imagem_produto = ImagemProdutoModel.buscar_imagem(imagem_produto_id)
        if imagem_produto:
            return imagem_produto.json()
        return {'mensagem': 'A imagem do produto não foi encontrada.'}, 404


    def delete(self, imagem_produto_id):
        imagem_produto = ImagemProdutoModel.buscar_imagens_produto(imagem_produto_id)
        if imagem_produto:
            try:
                imagem_produto.deletar_imagem()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "A imagem do produto foi deletada com sucesso"}
        return{"mensagem":"A imagem do produto não foi encontrada."}

class ImagemProdutoCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()
        imagem_produto = ImagemProdutoModel(**dados)
        try:
            imagem_produto.salvar_imagem()
        except:
            return {"mensagem":"Ocorreu um erro interno"}, 500
        return imagem_produto.json()