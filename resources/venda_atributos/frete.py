from flask_restful import Resource, reqparse
from models.venda_atributos.frete import FreteModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('prazo_entrega', type=str, required=True, help= "O campo 'prazo_entrega' precisa ser preenchido.")
argumentos.add_argument('valor_frete', type=str, required=True, help= "O campo 'desconto' precisa ser preenchido.")


class Fretes(Resource):

    def get(self):

        prazo_entregas = FreteModel.buscar_todos_fretes()
        return prazo_entregas

class Frete(Resource):

    def get(self, frete_id):
        
        prazo_entrega = FreteModel.buscar_frete(frete_id)
        if prazo_entrega:
            return prazo_entrega.json()
        return {'mensagem': 'A forma de pagamento não foi encontrada.'}, 404

    def put(self, frete_id):
        
        dados = argumentos.parse_args()

        prazo_entrega_encontrada = FreteModel.buscar_frete(frete_id)

        if prazo_entrega_encontrada:
            prazo_entrega_encontrada.atualizar_frete(**dados)
            prazo_entrega_encontrada.salvar_frete()
            return prazo_entrega_encontrada.json(), 200

        prazo_entrega = FreteModel( frete_id, **dados )

        try:
            prazo_entrega.salvar_frete()
        except:
            return {"Ocorreu um erro interno"}, 500
        return prazo_entrega.json(), 201

    def delete(self, frete_id):
        prazo_entrega = FreteModel.buscar_frete(frete_id)
        if prazo_entrega:
            try:
                prazo_entrega.deletar_frete()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "A forma de pagamento foi deletada com sucesso"}
        return{"mensagem":"A forma de pagamento não foi encontrada."}

class FreteCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()
        prazo_entrega = FreteModel(**dados)
        try:
            prazo_entrega.salvar_frete()
        except:
            return {"mensagem":"Ocorreu um erro interno"}, 500
        return prazo_entrega.json()