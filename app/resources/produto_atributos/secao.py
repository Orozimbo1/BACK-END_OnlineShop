from flask_restful import Resource, reqparse
from models.produto_atributos.secao import SecaoProdutoModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('nome_secao', type=str, required=True, help= "O campo 'nome_secao' precisa ser preenchido.")


class Secoes(Resource):

    def get(self):

        secoes = SecaoProdutoModel.buscar_todas_secoes()
        return secoes

class Secao(Resource):

    def get(self, secao_produto_id):
        
        secao = SecaoProdutoModel.buscar_secao(secao_produto_id)
        if secao:
            return secao.json()
        return {'mensagem': 'A seção não foi encontrada.'}, 404


    def delete(self, secao_produto_id):
        secao = SecaoProdutoModel.buscar_secao(secao_produto_id)
        if secao:
            try:
                secao.deletar_secao()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "A seção foi deletada com sucesso"}
        return{"mensagem":"A seção não foi encontrada."}

class SecaoCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()
        secao = SecaoProdutoModel(**dados)
        try:
            secao.salvar_secao()
        except:
            return {"mensagem":"Ocorreu um erro interno"}, 500
        return secao.json()