from sql_alquemy import engine
from flask_cors import CORS
from flask import Flask, jsonify
from flask_restful import Api
from resources.usuario import Usuario, UsuarioLogin, Usuarios, UsuarioCadastro, UsuarioLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from resources.venda_prod import VendaProdCadastro, VendasProd, VendaProd
from resources.venda import VendaCadastro, Vendas, Venda
from resources.produto_atributos.categoria import Categorias, Categoria, CategoriaCadastro
from resources.produto_atributos.cor import Cor, Cores, CorCadastro
from resources.produto_atributos.estilo import Estilos, Estilo, EstiloCadastro
from resources.produto_atributos.genero import Generos, Genero, GeneroCadastro
from resources.produto_atributos.imagens_produto import ImagensProdutos, ImagemProduto, ImagemProdutoCadastro
from resources.produto_atributos.qtd_estoque import QtdProdutos, QtdProduto, QtdProdutoCadastro
from resources.produto_atributos.secao import Secoes, Secao, SecaoCadastro
from resources.produto_atributos.tamanho import Tamanhos, Tamanho, TamanhoCadastro
from resources.produto import Produtos, Produto, ProdutoCadastro
from resources.loja import LojaLogin, Lojas, Loja, LojaCadastro, LojaLogout

app = Flask(__name__)

CORS(app)
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

## ROTAS DOS USUARIOS

api.add_resource(Usuarios, '/usuarios')
api.add_resource(Usuario, '/usuario/<int:usuario_id>')
api.add_resource(UsuarioCadastro, '/usuario/cadastro')
api.add_resource(UsuarioLogin, '/login')
api.add_resource(UsuarioLogout, '/logout')

## ROTAS DAS LOJAS

api.add_resource(Lojas, '/lojas')
api.add_resource(Loja, '/loja/<string:nome_fantasia>')
api.add_resource(LojaCadastro, '/loja/cadastro')
api.add_resource(LojaLogin, '/loja/login')
api.add_resource(LojaLogout, '/loja/logout' )

## ROTAS DAS VENDAS

api.add_resource(VendasProd, '/vendas-produtos')
api.add_resource(VendaProd, '/venda-produto/<int:venda_prod_id>')
api.add_resource(VendaProdCadastro, '/venda-produto/cadastro')
api.add_resource(Vendas, '/vendas')
api.add_resource(Venda, '/venda/<int:venda_id>')
api.add_resource(VendaCadastro, '/venda/cadastro')

## ROTAS DOS PRODUTOS

api.add_resource(Produtos, '/produtos')
api.add_resource(Produto, '/produto/<int:produto_id>')
api.add_resource(ProdutoCadastro, '/produto/cadastro')
api.add_resource(Categorias, '/categorias')
api.add_resource(Categoria, '/categoria/<int:categoria_produto_id>')
api.add_resource(CategoriaCadastro, '/categoria/cadastro')
api.add_resource(Cores, '/cores')
api.add_resource(Cor, '/cor/<int:cor_produto_id>')
api.add_resource(CorCadastro, '/cor/cadastro')
api.add_resource(Estilos, '/estilos')
api.add_resource(Estilo, '/estilo/<int:estilo_produto_id>')
api.add_resource(EstiloCadastro, '/estilo/cadastro')
api.add_resource(Generos, '/generos')
api.add_resource(Genero, '/genero/<int:genero_produto_id>')
api.add_resource(GeneroCadastro, '/genero/cadastro')
api.add_resource(ImagensProdutos, '/imagens-do-produto')
api.add_resource(ImagemProduto, '/imagem-do-produto/<int:imagem_produto_id>')
api.add_resource(ImagemProdutoCadastro, '/imagem-do-produto/cadastro')
api.add_resource(QtdProdutos, '/qtd-do-estoque')
api.add_resource(QtdProduto, '/qtd-do-estoque/<int:qtd_produto_id>')
api.add_resource(QtdProdutoCadastro, '/qtd-do-estoque/cadastro')
api.add_resource(Secoes, '/secoes')
api.add_resource(Secao, '/secao/<int:secao_produto_id>')
api.add_resource(SecaoCadastro, '/secao/cadastro')
api.add_resource(Tamanhos, '/tamanhos')
api.add_resource(Tamanho, '/tamanho/<int:tamanho_produto_id>')
api.add_resource(TamanhoCadastro, '/tamanho/cadastro')

if __name__ == '__main__':
    app.run(debug=True)