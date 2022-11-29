import dotenv
import os
from database import engine
from flask_cors import CORS , cross_origin
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from resources.usuario import Usuario, UsuarioLogin, Usuarios, UsuarioCadastro, UsuarioLogout
from resources.venda_prod import VendaProdCadastro, VendasProd, VendaProd
from resources.venda import VendaCadastro, Vendas, Venda
from resources.venda_atributos.frete import Fretes, Frete, FreteCadastro
from resources.venda_atributos.pagamento import FormaPagamentos, FormaPagamento, FormaPagamentoCadastro
from resources.produto_atributos.categoria import Categorias, Categoria, CategoriaCadastro
from resources.produto_atributos.estilo import Estilos, Estilo, EstiloCadastro
from resources.produto_atributos.genero import Generos, Genero, GeneroCadastro
from resources.produto_atributos.imagens_produto import ImagensProdutos, ImagemProduto, ImagemProdutoCadastro
from resources.produto_atributos.secao import Secoes, Secao, SecaoCadastro
from resources.produto import Produtos, Produto, ProdutoCadastro, ProdutoFiltro
from resources.loja import LojaLogin, Lojas, Loja, LojaCadastro, LojaLogout
from resources.loja_atributos.cep import CepLojas, CepLoja, CepLojaCadastro
from resources.loja_atributos.contato import ContatoLojas, ContatoLoja, ContatoLojaCadastro
from resources.usuario_atributos.cep import CepUsuarios, CepUsuario, CepUsuarioCadastro
from resources.usuario_atributos.contato import ContatoUsuarios, ContatoUsuario, ContatoUsuarioCadastro

app = Flask(__name__)


CORS(app,supports_credentials=True)

dotenv.load_dotenv(dotenv.find_dotenv())
app.config['SQLALCHEMY_DATABASE_URI'] = engine
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_BLACKLIST_ENABLE'] = True
api = Api(app)
jwt = JWTManager(app)

@cross_origin(origin='*')
def sucess():
  return jsonify({'success': 'ok'})



@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'mensagem': 'Você já se deslogou.'}), 401


## ROTAS DOS USUARIOS

api.add_resource(Usuarios, '/usuarios')
api.add_resource(Usuario, '/usuario/<int:usuario_id>')
api.add_resource(UsuarioCadastro, '/usuario/cadastro')
api.add_resource(UsuarioLogin, '/login')
api.add_resource(UsuarioLogout, '/logout')
api.add_resource(CepUsuarios, '/usuarios-enderecos')
api.add_resource(CepUsuario, '/usuario-endereco/<int:endereco_usuario_id>')
api.add_resource(CepUsuarioCadastro, '/usuario-endereco/cadastro')
api.add_resource(ContatoUsuarios, '/usuarios-contatos')
api.add_resource(ContatoUsuario, '/usuario-contato/<int:contato_usuario_id>')
api.add_resource(ContatoUsuarioCadastro, '/usuario-contato/cadastro')


## ROTAS DAS LOJAS

api.add_resource(Lojas, '/lojas')
api.add_resource(Loja, '/loja/<int:loja_id>')
api.add_resource(LojaCadastro, '/loja/cadastro')
api.add_resource(LojaLogin, '/loja/login')
api.add_resource(LojaLogout, '/loja/logout')
api.add_resource(CepLojas, '/lojas-enderecos')
api.add_resource(CepLoja, '/loja-endereco/<int:endereco_loja_id>')
api.add_resource(CepLojaCadastro, '/loja-endereco/cadastro')
api.add_resource(ContatoLojas, '/lojas-contatos')
api.add_resource(ContatoLoja, '/loja-contato/<int:contato_loja_id>')
api.add_resource(ContatoLojaCadastro, '/loja-contato/cadastro')


## ROTAS DAS VENDAS

api.add_resource(VendasProd, '/vendas-produtos')
api.add_resource(VendaProd, '/venda-produto/<int:venda_prod_id>')
api.add_resource(VendaProdCadastro, '/venda-produto/cadastro')
api.add_resource(Vendas, '/vendas')
api.add_resource(Venda, '/venda/<int:venda_id>')
api.add_resource(VendaCadastro, '/venda/cadastro')
api.add_resource(Fretes, '/fretes')
api.add_resource(Frete, '/frete/<int:frete_id>')
api.add_resource(FreteCadastro, '/frete/cadastro')
api.add_resource(FormaPagamentos, '/forma-de-pagamentos')
api.add_resource(FormaPagamento, '/forma-de-pagamento/<int:pagamento_id>')
api.add_resource(FormaPagamentoCadastro, '/forma-de-pagamento/cadastro')

## ROTAS DOS PRODUTOS

api.add_resource(Produtos, '/produtos')
api.add_resource(Produto, '/produto/<int:produto_id>')
api.add_resource(ProdutoCadastro, '/produto/cadastro')
api.add_resource(ProdutoFiltro, '/produto-filtro/<int:genero_produto_id>')
api.add_resource(Categorias, '/categorias')
api.add_resource(Categoria, '/categoria/<int:categoria_produto_id>')
api.add_resource(CategoriaCadastro, '/categoria/cadastro')
api.add_resource(Estilos, '/estilos')
api.add_resource(Estilo, '/estilo/<int:estilo_produto_id>')
api.add_resource(EstiloCadastro, '/estilo/cadastro')
api.add_resource(Generos, '/generos')
api.add_resource(Genero, '/genero/<int:genero_produto_id>')
api.add_resource(GeneroCadastro, '/genero/cadastro')
api.add_resource(ImagensProdutos, '/imagens-do-produto')
api.add_resource(ImagemProduto, '/imagem-do-produto/<int:imagem_produto_id>')
api.add_resource(ImagemProdutoCadastro, '/imagem-do-produto/cadastro')
api.add_resource(Secoes, '/secoes')
api.add_resource(Secao, '/secao/<int:secao_produto_id>')
api.add_resource(SecaoCadastro, '/secao/cadastro')


