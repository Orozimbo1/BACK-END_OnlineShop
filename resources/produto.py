from multiprocessing import connection
from sqlite3 import connect
import sqlite3
from flask_restful import Resource, reqparse
from models.produto import ProdutoModel
import sqlite3

def normalizar_path_params(genero=None,
                            secao=None,
                            categoria=None,
                            estilo=None,
                            cor=None,
                            tamanho=None,
                            preco_min= 0,
                            preco_max = 20000,
                            limit = 50,
                            offset = 0, **dados):
    if genero:
        return{ genero: genero,
                secao: secao,
                categoria: categoria,
                estilo: estilo,
                cor: cor,
                tamanho: tamanho,
                preco_min: preco_min,
                preco_max: preco_max,
                limit: limit,
                offset: offset}

    return  {   secao: secao,
                categoria: categoria,
                estilo: estilo,
                cor: cor,
                tamanho: tamanho,
                preco_min: preco_min,
                preco_max: preco_max,
                limit: limit,
                offset: offset}

path_params = reqparse.RequestParser()
path_params.add_argument('genero', type=str)
path_params.add_argument('secao', type=str)
path_params.add_argument('categoria', type=str)
path_params.add_argument('estilo', type=str)
path_params.add_argument('nome', type=str)
path_params.add_argument('cor', type=str)
path_params.add_argument('tamanho', type=str)
path_params.add_argument('preco_min', type=float)
path_params.add_argument('preco_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)



class Produtos(Resource):

    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalizar_path_params(**dados_validos)
        
        if not parametros.get('genero'):
            consulta = "SELECT * FROM produtos WHERE (preco > ? and preco < ?) LIMIT ? OFFSET ?"
            tupla = tupla([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)
        else:
            consulta = "SELECT * FROM produtos WHERE genero =? and (preco > ? and preco < ?) LIMIT ? OFFSET ?"
            tupla = tupla([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)
        
        produtos = []
        for linha in resultado:
            produtos.append({
                    "genero" : linha[0],
                    "secao" : linha [1],
                    "categoria" : linha[2],
                    "estilo" : linha[3],
                    "nome": linha[4],
                    "descricao" :linha[5],
                    "cor" : linha[6],
                    "tamanho" : linha[7],
                    "preco" : linha[8]
                    })

        return {"produtos": produtos}

class Produto(Resource):

    argumentos = reqparse.RequestParser()
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

    def get(self, produto_id):
        
        produto = ProdutoModel.buscar_produtos(produto_id)
        if produto:
            return produto.json()
        return {'mensagem': 'Produto não encontrado.'}, 404

    def post(self, produto_id):

        if ProdutoModel.buscar_produtos(produto_id):
            return {"mensagem":"Produto '{}' já existente !".format(produto_id)}, 404

        dados = Produto.argumentos.parse_args()
        produto = ProdutoModel(produto_id, **dados)
        try:
            produto.salvar_produto()
        except:
            return {"mensagem":"Ocorreu um erro interno"}, 500
        return produto.json()

    def put(self, produto_id):
        
        dados = Produto.argumentos.parse_args()

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