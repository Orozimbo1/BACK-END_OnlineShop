from flask_restful import Resource, reqparse
from models.usuario import UsuarioModel
from models.venda import VendaModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('usuario_id', type=int, required=True, help= "O campo 'usuario_id' precisa ser preenchido.")


class Vendas(Resource):

    def get(self):

        vendas = VendaModel.buscar_todas_vendas()
        return vendas

class Venda(Resource):

    def get(self, venda_id):
        
        venda = VendaModel.buscar_venda(venda_id)
        if venda:
            return venda.json()
        return {'mensagem': 'A venda não foi encontrada.'}, 404


    def delete(self, venda_id):
        venda = VendaModel.buscar_venda(venda_id)
        if venda:
            try:
                venda.deletar_venda()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "A venda foi deletada com sucesso"}
        return{"mensagem":"A venda não foi encontrada."}

class VendaCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()
        venda = VendaModel(**dados)
        usuario = UsuarioModel.buscar_usuario(dados.get('usuario_id'))
        if usuario:
            try:
                venda.salvar_venda()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return venda.json()
        return {"mensagem": "Esse usuário não existe. Por favor insira um 'id' válido."}