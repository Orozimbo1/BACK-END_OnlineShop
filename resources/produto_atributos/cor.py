from flask_restful import Resource, reqparse
from models.produto_atributos.cor import CorProdutoModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('nome_cor', type=str, required=True, help= "O campo 'nome_cor' precisa ser preenchido.")
argumentos.add_argument('produto_id', type=str, help= "O campo 'produto_id' precisa ser preenchido.")

class Cores(Resource):

    def get(self):

        cores = CorProdutoModel.buscar_todas_cores()
        return cores

class Cor(Resource):

    def get(self, cor_produto_id):
        
        cor = CorProdutoModel.buscar_cor(cor_produto_id)
        if cor:
            return cor.json()
        return {'mensagem': 'A cor não foi encontrada.'}, 404


    def delete(self, cor_produto_id):
        cor = CorProdutoModel.buscar_cor(cor_produto_id)
        if cor:
            try:
                cor.deletar_cor()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "A cor foi deletada com sucesso"}
        return{"mensagem":"A cor não foi encontrada."}

class CorCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()
        cor = CorProdutoModel(**dados)
        try:
            cor.salvar_cor()
        except:
            return {"mensagem":"Ocorreu um erro interno"}, 500
        return cor.json()