from sql_alquemy import engine
from flask import Flask, jsonify
from flask_restful import Api
from resources.usuario import Usuario, UsuarioLogin, Usuarios, UsuarioCadastro, UsuarioLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from resources.produto import Produtos, Produto, ProdutoCadastro
from resources.loja import Lojas, Loja, LojaCadastro
from resources.venda import Venda, Vendas, VendaCadastro

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = engine
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'asdfghjklç'
app.config['JWT_BLACKLIST_ENABLE'] = True
api = Api(app)
jwt = JWTManager(app)

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
api.add_resource(UsuarioCadastro, '/usuario/cadastro')
api.add_resource(UsuarioLogin, '/login')
api.add_resource(UsuarioLogout, '/logout')
api.add_resource(Produtos, '/produtos')
api.add_resource(Produto, '/produto/<int:produto_id>')
api.add_resource(ProdutoCadastro, '/produto/cadastro')
api.add_resource(Lojas, '/lojas')
api.add_resource(Loja, '/loja/<string:nome_fantasia>')
api.add_resource(LojaCadastro, '/loja/cadastro')
api.add_resource(VendaCadastro, '/venda/cadastro')
api.add_resource(Vendas, '/vendas')
api.add_resource(Venda, '/venda/<int:venda_id>')

if __name__ == '__main__':
    app.run(debug=True)