from flask import Flask
from flask_restful import Api
from resources.usuario import Usuario, Usuarios
from resources.produto import Produtos, Produto
from resources.loja import Lojas, Loja

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def cria_banco():
    banco.create_all()

@app.route('/')
def hello():
    return 'Hello world'

api.add_resource(Usuarios, '/usuarios')
api.add_resource(Usuario, '/usuario/<int:usuario_id>')
api.add_resource(Produtos, '/produtos')
api.add_resource(Produto, '/produto/<int:produto_id>')
api.add_resource(Lojas, '/lojas')
api.add_resource(Loja, '/loja/<string:loja_id>')


if __name__ == '__main__':
    from sql_alquemy import banco
    banco.init_app(app)
    app.run(debug=True)