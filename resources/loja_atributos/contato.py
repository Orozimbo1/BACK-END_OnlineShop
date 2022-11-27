from flask_restful import Resource, reqparse
from models.loja_atributos.contato import ContatoLojaModel



argumentos = reqparse.RequestParser()
argumentos.add_argument('loja_id', type=int)
argumentos.add_argument('celular', type=str)
argumentos.add_argument('nome')

class ContatoLojas(Resource):

    def get(self):
        contatos = ContatoLojaModel.buscar_todos_contatos()
        return contatos

class ContatoLoja(Resource):

    def get(self, contato_loja_id):
        
        contato = ContatoLojaModel.buscar_contato_por_id(contato_loja_id)
        if contato:
            return contato.json()
        return {'mensagem': 'Contato não encontrado.'}, 404

    def put(self, contato_loja_id):
        
        dados = argumentos.parse_args()

        contato = ContatoLojaModel.buscar_contato_por_id(contato_loja_id)
        if contato:
            contato.atualizar_contato(**dados)
            contato.salvar_contato()
            return contato.json(), 200
        contato =ContatoLojaModel(contato_loja_id, **dados )

        try:
            contato.salvar_loja()
        except:
            return {"Ocorreu um erro interno"}, 500
        return contato.json(), 201

    def delete(self, contato_loja_id):
        contato = ContatoLojaModel.buscar_contato_por_id(contato_loja_id)
        if contato:
            try:
                contato.deletar_contato()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "Contato deletado com sucesso."}
        return{"mensagem":"Contato não encontrado"}

class ContatoLojaCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()

        contato = ContatoLojaModel(**dados)
        try:
            contato.salvar_contato()
        except:
            return {'mensagem': 'Houve um erro tentando salvar contato.'}, 500
        return contato.json()
