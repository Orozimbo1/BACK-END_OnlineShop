from flask_restful import Resource, reqparse
from models.usuario_atributos.contato import ContatoUsuarioModel



argumentos = reqparse.RequestParser()
argumentos.add_argument('celular', type=str)
argumentos.add_argument('titular_celular')
argumentos.add_argument('telefone_fixo')
argumentos.add_argument('titular_telefone_fixo', type=str)
argumentos.add_argument('instagram', type=str)
argumentos.add_argument('facebook', type=str)
argumentos.add_argument('linkedin', type=str)

class ContatoUsuarios(Resource):

    def get(self):
        contatos = ContatoUsuarioModel.buscar_todos_contatos()
        return contatos

class ContatoUsuario(Resource):

    def get(self, contato_usuario_id):
        
        contato = ContatoUsuarioModel.buscar_contato_por_id(contato_usuario_id)
        if contato:
            return contato.json()
        return {'mensagem': 'Contato não encontrado.'}, 404

    def put(self, contato_usuario_id):
        
        dados = argumentos.parse_args()

        contato = ContatoUsuarioModel.buscar_contato_por_id(contato_usuario_id)
        if contato:
            contato.atualizar_contato(**dados)
            contato.salvar_contato()
            return contato.json(), 200
        contato =ContatoUsuarioModel(contato_usuario_id, **dados )

        try:
            contato.salvar_usuario()
        except:
            return {"Ocorreu um erro interno"}, 500
        return contato.json(), 201

    def delete(self, contato_usuario_id):
        contato = ContatoUsuarioModel.buscar_contato_por_id(contato_usuario_id)
        if contato:
            try:
                contato.deletar_contato()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "Contato deletado com sucesso."}
        return{"mensagem":"Contato não encontrado"},404

class ContatoUsuarioCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()

        contato = ContatoUsuarioModel(**dados)
        try:
            contato.salvar_contato()
        except:
            return {'mensagem': 'Houve um erro tentando salvar contato.'}, 500
        return contato.json()