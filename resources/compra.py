from flask_restful import Resource, reqparse
from models.compra import CompraModel
from models.usuario import UsuarioModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('usuario_id', type=int,required= True, help= " O campo 'usuario' precisa ser preenchido.")
argumentos.add_argument('produto_id', type=int,required= True, help= " O campo 'produto' precisa ser preenchido.")


class Compras(Resource):

    def get(self):

        compras = CompraModel.buscar_todas_compras()
        return compras

class Compra(Resource):

    def get(self, compra_id):
        
        compra = CompraModel.buscar_compras(compra_id)
        if compra:
            return compra.json()
        return {'mensagem': 'Compra não encontrado.'}, 404

    def delete(self, compra_id):
        compra = CompraModel.buscar_compras(compra_id)
        if compra:
            try:
                compra.deletar_compra()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "Compra deletada com sucesso"}
        return{"mensagem":"Compra não encontrada"}

class CompraCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()
        compra = CompraModel(**dados)
        usuario = UsuarioModel.buscar_usuario(dados.get('usuario_id'))
        if usuario:
            try:
                compra.salvar_compra()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return compra.json()
        return {"mensagem":"Usuário não encontrado."}, 500