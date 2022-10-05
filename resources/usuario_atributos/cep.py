from flask_restful import Resource, reqparse
from models.usuario_atributos.cep import CepUsuarioModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('local_endereco', type=str)
argumentos.add_argument('CEP', type=str)
argumentos.add_argument('cidade', type=str)
argumentos.add_argument('logradouro', type=str)
argumentos.add_argument('rua', type=str)
argumentos.add_argument('numero', type=int)

class CepUsuarios(Resource):

    def get(self):
        enderecos = CepUsuarioModel.buscar_todos_enderecos()
        return enderecos

class CepUsuario(Resource):

    def get(self, endereco_usuario_id):
        
        endereco = CepUsuarioModel.buscar_endereco_por_id(endereco_usuario_id)
        if endereco:
            return endereco.json()
        return {'mensagem': 'Endereco não encontrado.'}, 404

    def put(self, endereco_usuario_id):
        
        dados = argumentos.parse_args()

        endereco = CepUsuarioModel.buscar_endereco_por_id(endereco_usuario_id)
        if endereco:
            endereco.atualizar_endereco(**dados)
            endereco.salvar_endereco()
            return endereco.json(), 200
        endereco =CepUsuarioModel(endereco_usuario_id, **dados )

        try:
            endereco.salvar_endereco()
        except:
            return {"Ocorreu um erro interno"}, 500
        return endereco.json(), 201

    def delete(self, endereco_usuario_id):
        endereco = CepUsuarioModel.buscar_endereco_por_id(endereco_usuario_id)
        if endereco:
            try:
                endereco.deletar_endereco()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "Endereço deletado com sucesso"}
        return{"mensagem":"Endereço não encontrado"},404

class CepUsuarioCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()

        endereco = CepUsuarioModel(**dados)
        try:
            endereco.salvar_endereco()
        except:
            return {'mensagem': 'Houve um erro tentando salvar o endereço.'}, 500
        return endereco.json()