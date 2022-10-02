from flask_restful import Resource, reqparse
from models.produto_atributos.tamanho import TamanhoProdutoModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('nome_tamanho', type=str, required=True, help= "O campo 'nome_tamanho' precisa ser preenchido.")


class Tamanhos(Resource):

    def get(self):

        tamanhos = TamanhoProdutoModel.buscar_todos_tamanhos
        return tamanhos

class Tamanho(Resource):

    def get(self, tamanho_produto_id):
        
        tamanho = TamanhoProdutoModel.buscar_tamanho(tamanho_produto_id)
        if tamanho:
            return tamanho.json()
        return {'mensagem': 'O tamanho não foi encontrado.'}, 404


    def delete(self, tamanho_produto_id):
        tamanho = TamanhoProdutoModel.buscar_tamanho(tamanho_produto_id)
        if tamanho:
            try:
                tamanho.deletar_tamanho()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "O tamanho foi deletado com sucesso"}
        return{"mensagem":"O tamanho não foi encontrado."}

class TamanhoCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()
        tamanho = TamanhoProdutoModel(**dados)
        try:
            tamanho.salvar_tamanho()
        except:
            return {"mensagem":"Ocorreu um erro interno"}, 500
        return tamanho.json()