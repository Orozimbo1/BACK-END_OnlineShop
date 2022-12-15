from flask_restful import Resource, reqparse
from models.venda_atributos.pagamento import PagamentoModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('forma_pagamento', type=str, required=True, help= "O campo 'forma_pagamento' precisa ser preenchido.")
argumentos.add_argument('desconto', type=str, required=True, help= "O campo 'desconto' precisa ser preenchido.")


class FormaPagamentos(Resource):

    def get(self):

        forma_pagamentos = PagamentoModel.buscar_todos_pagamentos()
        return forma_pagamentos

class FormaPagamento(Resource):

    def get(self, pagamento_id):
        
        forma_pagamento = PagamentoModel.buscar_pagamento(pagamento_id)
        if forma_pagamento:
            return forma_pagamento.json()
        return {'mensagem': 'A forma de pagamento não foi encontrada.'}, 404

    def put(self, pagamento_id):
        
        dados = argumentos.parse_args()

        forma_pagamento_encontrada = PagamentoModel.buscar_pagamento(pagamento_id)

        if forma_pagamento_encontrada:
            forma_pagamento_encontrada.atualizar_pagamento(**dados)
            forma_pagamento_encontrada.salvar_pagamento()
            return forma_pagamento_encontrada.json(), 200

        forma_pagamento = PagamentoModel( pagamento_id, **dados )

        try:
            forma_pagamento.salvar_pagamento()
        except:
            return {"Ocorreu um erro interno"}, 500
        return forma_pagamento.json(), 201

    def delete(self, pagamento_id):
        forma_pagamento = PagamentoModel.buscar_pagamento(pagamento_id)
        if forma_pagamento:
            try:
                forma_pagamento.deletar_pagamento()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "A forma de pagamento foi deletada com sucesso"}
        return{"mensagem":"A forma de pagamento não foi encontrada."}

class FormaPagamentoCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()
        forma_pagamento = PagamentoModel(**dados)
        try:
            forma_pagamento.salvar_pagamento()
        except:
            return {"mensagem":"Ocorreu um erro interno"}, 500
        return forma_pagamento.json()