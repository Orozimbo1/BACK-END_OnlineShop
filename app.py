from importlib.resources import Resource
from flask import Flask
from flask_restful import Api
from resources.usuario import Usuario, Usuarios
from resources.produtos import Produtos, Produto

app = Flask(__name__)
api = Api(app)

@app.route('/')
def hello():
    return 'Hello world'

api.add_resource(Usuarios, '/usuarios')
api.add_resource(Usuario, '/usuario/<int:usuario_id>')
api.add_resource(Produtos, '/produtos')
api.add_resource(Produto, '/produto/<int:produto_id>')

if __name__ == '__main__':
    app.run(debug=True)