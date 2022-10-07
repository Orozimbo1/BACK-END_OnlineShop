from flask_restful import Resource, reqparse
from models.produto_atributos.genero import GeneroProdutoModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('nome_genero', type=str, required=True, help= "O campo 'nome_genero' precisa ser preenchido.")


class Generos(Resource):

    def get(self):

        generos = GeneroProdutoModel.buscar_todos_generos()
        return generos

class Genero(Resource):

    def get(self, genero_produto_id):
        
        genero = GeneroProdutoModel.buscar_genero(genero_produto_id)
        if genero:
            return genero.json()
        return {'mensagem': 'O genero não foi encontrado.'}, 404


    def delete(self, genero_produto_id):
        genero = GeneroProdutoModel.buscar_genero(genero_produto_id)
        if genero:
            try:
                genero.deletar_genero()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "O genero foi deletado com sucesso"}
        return{"mensagem":"O genero não foi encontrado."}

class GeneroCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()
        genero = GeneroProdutoModel(**dados)
        try:
            genero.salvar_genero()
        except:
            return {"mensagem":"Ocorreu um erro interno"}, 500
        return genero.json()