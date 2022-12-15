from flask_restful import Resource, reqparse
from models.produto_atributos.categoria import CategoriaProdutoModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('nome_categoria', type=str, required=True, help= "O campo 'nome_categoria' precisa ser preenchido.")


class Categorias(Resource):

    def get(self):

        categorias = CategoriaProdutoModel.buscar_todas_categorias()
        return categorias

class Categoria(Resource):

    def get(self, categoria_produto_id):
        
        categoria = CategoriaProdutoModel.buscar_categoria(categoria_produto_id)
        if categoria:
            return categoria.json()
        return {'mensagem': 'A categoria não foi encontrada.'}, 404


    def delete(self, categoria_produto_id):
        categoria = CategoriaProdutoModel.buscar_categoria(categoria_produto_id)
        if categoria:
            try:
                categoria.deletar_categoria()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "A categoria foi deletada com sucesso"}
        return{"mensagem":"A categoria não foi encontrada."}

class CategoriaCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()
        categoria = CategoriaProdutoModel(**dados)
        try:
            categoria.salvar_categoria()
        except:
            return {"mensagem":"Ocorreu um erro interno"}, 500
        return categoria.json()