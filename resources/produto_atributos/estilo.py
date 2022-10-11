from flask_restful import Resource, reqparse
from models.produto_atributos.estilo import EstiloProdutoModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('nome_estilo', type=str, required=True, help= "O campo 'nome_estilo' precisa ser preenchido.")


class Estilos(Resource):

    def get(self):

        estilos = EstiloProdutoModel.buscar_todos_estilos()
        return estilos

class Estilo(Resource):

    def get(self, estilo_produto_id):
        
        estilo = EstiloProdutoModel.buscar_estilo(estilo_produto_id)
        if estilo:
            return estilo.json()
        return {'mensagem': 'O estilo não foi encontrado.'}, 404


    def delete(self, estilo_produto_id):
        estilo = EstiloProdutoModel.buscar_estilo(estilo_produto_id)
        if estilo:
            try:
                estilo.deletar_estilo()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "O estilo foi deletado com sucesso"}
        return{"mensagem":"O estilo não foi encontrado."}

class EstiloCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()
        estilo = EstiloProdutoModel(**dados)
        try:
            estilo.salvar_estilo()
        except:
            return {"mensagem":"Ocorreu um erro interno"}, 500
        return estilo.json()