from flask import Flask, jsonify
from flask_restful import Api
from resources.usuario import Usuario, UsuarioLogin, Usuarios, UsuarioCadastro, UsuarioLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from resources.usuario import Usuario, Usuarios
from resources.produto import Produtos, Produto
from resources.loja import Lojas, Loja, LojaCadastro

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'asdfghjklç'
app.config['JWT_BLACKLIST_ENABLE'] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def cria_banco():
    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'mensagem': 'Voçê já se deslogou.'}), 401

@app.route('/')
def hello():
    return 'Hello world'

api.add_resource(Usuarios, '/usuarios')
api.add_resource(Usuario, '/usuario/<int:usuario_id>')
api.add_resource(UsuarioCadastro, '/cadastro')
api.add_resource(UsuarioLogin, '/login')
api.add_resource(UsuarioLogout, '/logout')
api.add_resource(Produtos, '/produtos')
api.add_resource(Produto, '/produto/<int:produto_id>')
api.add_resource(Lojas, '/lojas')
api.add_resource(Loja, '/loja/<string:loja_id>')
api.add_resource(LojaCadastro, '/loja/cadastrar-loja/<string:loja_id>')


if __name__ == '__main__':
    from sql_alquemy import banco
    banco.init_app(app)
    app.run(debug=True)