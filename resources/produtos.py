from flask_restful import Resource, reqparse

produtos = [
    {
        'produto_id': 1,
        'genero': 'masculina',
        'secao': 'adulto',
        'categoria': 'roupas',
        'estilo': 'casual',
        'nome': 'camisa',
        'qtd_estoque': 20,
        'cor': ['branco', 'azul', 'vermelho'],
        'tamanho': ['P', 'M', 'G']
    },
    {
        'produto_id': 2,
        'genero': 'masculina',
        'secao': 'adulto',
        'categoria': 'roupas',
        'estilo': 'casual',
        'nome': 'camisa',
        'qtd_estoque': 20,
        'cor': ['branco', 'azul', 'vermelho'],
        'tamanho': ['P', 'M', 'G']
    },
]

class Produtos(Resource):

    def get(self):
        return {'produtos': produtos}

class Produto(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('genero')
    argumentos.add_argument('secao')
    argumentos.add_argument('categoria')
    argumentos.add_argument('estilo')
    argumentos.add_argument('nome')
    argumentos.add_argument('qtd_estoque')
    argumentos.add_argument('cor')
    argumentos.add_argument('tamanho')

    def buscar_produtos(produto_id):
        for produto in produtos:
            if produto['produto_id'] == produto_id:
                return produto
        return None

    def get(self, produto_id):
        
        produto = Produto.buscar_produtos(produto_id)
        if produto:
            return produto
        return {'mensagem': 'Produto não encontrado.'}, 404

    def post(self, produto_id):

        dados = Produto.argumentos.parse_args()
        novo_produto = { 'produto_id': produto_id, **dados }

        produtos.append(novo_produto)
        return novo_produto, 201

    def put(self, produto_id):
        
        dados = Produto.argumentos.parse_args()
        novo_produto = { 'produto_id': produto_id, **dados }

        produto = Produto.buscar_produtos(produto_id)
        if produto:
            produto.update(novo_produto)
            return novo_produto, 200

        produtos.append(novo_produto)
        return novo_produto, 201

    def delete(self, produto_id):
        global produtos
        produtos = [produto for produto in produtos if produto['produto_id'] != produto_id]
        return {"mensagem":"Produto deletado com sucesso"}, 200