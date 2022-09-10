from flask_restful import Resource, reqparse
from models.loja import LojaModel
from models.produto import ProdutoModel
import sqlite3

argumentos = reqparse.RequestParser()
argumentos.add_argument('loja', type=str,required= True, help="Todo produto deve pertencer à uma loja.")
argumentos.add_argument('genero', type=str,required= True, help= " O campo 'Gênero' precisa ser preenchido")
argumentos.add_argument('secao', type=str,required= True, help= " O campo 'Seção' precisa ser preenchido")
argumentos.add_argument('categoria', type=str,required= True, help= " O campo 'Categoria' precisa ser preenchido")
argumentos.add_argument('estilo', type=str,required= True, help= " O campo 'Estilo' precisa ser preenchido")
argumentos.add_argument('nome', type=str,required= True, help= " O campo 'Nome' precisa ser preenchido")
argumentos.add_argument('descricao', type=str,)
argumentos.add_argument('qtd_estoque', type=int,required= True, help= " O campo 'Quantidade em estoque' precisa ser preenchido")
argumentos.add_argument('cor', type=str,required= True, help= " O campo 'Cor' precisa ser preenchido")
argumentos.add_argument('tamanho', type=str,required= True, help= " O campo 'Tamanho' precisa ser preenchido")
argumentos.add_argument('preco', type=float,required= True, help= " O campo 'Preço' precisa ser preenchido")

# def normalizar_caminho_parametros(genero=None,
#                             secao=None,
#                             categoria=None,
#                             estilo=None,
#                             cor=None,
#                             tamanho=None,
#                             preco_min= 0,
#                             preco_max = 20000,
#                             limit = 10,
#                             offset = 0, **dados):
    # if genero:
    #     return{ 
    #             genero: genero,
                # secao: secao,
                # categoria: categoria,
                # estilo: estilo,
                # cor: cor,
                # tamanho: tamanho,
        #         preco_min: preco_min,
        #         preco_max: preco_max,
        #         limit: limit,
        #         offset: offset
        # }

    # return  {   
                # secao: secao,
                # categoria: categoria,
                # estilo: estilo,
                # cor: cor,
                # tamanho: tamanho,
            #     preco_min: preco_min,
            #     preco_max: preco_max,
            #     limit: limit,
            #     offset: offset
            # }

# caminho_parametros = reqparse.RequestParser()
# caminho_parametros.add_argument('genero', type=str)
# caminho_parametros.add_argument('secao', type=str)
# caminho_parametros.add_argument('categoria', type=str)
# caminho_parametros.add_argument('estilo', type=str)
# caminho_parametros.add_argument('nome', type=str)
# caminho_parametros.add_argument('cor', type=str)
# caminho_parametros.add_argument('tamanho', type=str)
# caminho_parametros.add_argument('preco_min', type=float)
# caminho_parametros.add_argument('preco_max', type=float)
# caminho_parametros.add_argument('limit', type=float)
# caminho_parametros.add_argument('offset', type=float)



class Produtos(Resource):

    def get(self):

        return {"Produtos": [produto.json() for produto in ProdutoModel.query.all()]}

        # connection = sqlite3.connect('banco.db')
        # cursor = connection.cursor()

        # dados = caminho_parametros.parse_args()
        # dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        # parametros = normalizar_caminho_parametros(**dados_validos)
        
        # if not parametros.get('genero'):
        #     consulta = "SELECT * FROM produtos WHERE (preco >= ? or preco <= ?) LIMIT ? OFFSET ?"
        #     tupla = tuple([parametros[chave] for chave in parametros])
        #     resultado = cursor.execute(consulta, tupla)
        # else:
        #     consulta = "SELECT * FROM produtos WHERE (preco > ? or preco < ?) or genero = ?  LIMIT ? OFFSET ?"
        #     tupla = tuple([parametros[chave] for chave in parametros])
        #     resultado = cursor.execute(consulta, tupla)
        
        # produtos = []
        # for linha in resultado:
        #     produtos.append({
        #             "produto_id" : linha[0],
        #             "genero" : linha[1],
        #             "secao" : linha [2],
        #             "categoria" : linha[3],
        #             "estilo" : linha[4],
        #             "nome": linha[5],
        #             "descricao" :linha[6],
        #             "qtd_estoque" : linha[7],
        #             "cor" : linha[8],
        #             "tamanho" : linha[9],
        #             "preco" : linha[10]
        #             })

        # return {"produtos": produtos}

class Produto(Resource):

    def get(self, produto_id):
        
        produto = ProdutoModel.buscar_produtos(produto_id)
        if produto:
            return produto.json()
        return {'mensagem': 'Produto não encontrado.'}, 404

    def put(self, produto_id):
        
        dados = argumentos.parse_args()

        produto_encontrado = ProdutoModel.buscar_produtos(produto_id)
        if produto_encontrado:
            produto_encontrado.atualizar_produto(**dados)
            produto_encontrado.salvar_produto()
            return produto_encontrado.json(), 200

        produto = ProdutoModel( produto_id, **dados )

        try:
            # return {"Mensagem":"Aoba"}
            produto.salvar_produto()
        except:
            return {"Ocorreu um erro interno"}, 500
        return produto.json(), 201

    def delete(self, produto_id):
        produto = ProdutoModel.buscar_produtos(produto_id)
        if produto:
            try:
                produto.deletar_produto()
            except:
                return {"mensagem":"Ocorreu um erro interno"}, 500
            return{"mensagem": "Produto deletado com sucesso"}
        return{"mensagem":"Produto não encontrado"}

class ProdutoCadastro(Resource):

    def post(self):

        dados = argumentos.parse_args()
        produto = ProdutoModel(**dados)
        if not LojaModel.buscar_lojas(dados['loja']):
            return {"mensagem": "A loja '{}' não existe.". format(dados['loja'])}
        try:
            produto.salvar_produto()
        except:
            return {"mensagem":"Ocorreu um erro interno"}, 500
        return produto.json()