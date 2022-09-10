from sql_alquemy import banco

class ProdutoModel(banco.Model):
    __tablename__ = 'produtos'

    produto_id = banco.Column(banco.Integer, primary_key=True)
    genero = banco.Column(banco.String(80))
    secao = banco.Column(banco.String(80))
    categoria = banco.Column(banco.String(100))
    estilo = banco.Column(banco.String(80))
    nome = banco.Column(banco.String(40))
    descricao = banco.Column(banco.String(600))
    qtd_estoque = banco.Column(banco.Integer)
    cor = banco.Column(banco.String(10))
    tamanho = banco.Column(banco.String(10))
    preco = banco.Column(banco.Float(precision=2))

    def __init__(self, genero, secao, categoria, estilo, nome, descricao, qtd_estoque, cor, tamanho, preco):
        self.genero = genero
        self.secao = secao
        self.categoria = categoria
        self.estilo = estilo
        self.nome = nome
        self.descricao = descricao
        self.qtd_estoque = qtd_estoque
        self.cor = cor
        self.tamanho = tamanho
        self.preco = preco
    
    def json(self):
        return {
            'produto_id': self.produto_id,
            'genero': self.genero,
            'secao': self.secao,
            'categoria': self.categoria,
            'estilo': self.estilo,
            'nome': self.nome,
            'descricao': self.descricao,
            'qtd_estoque': self.qtd_estoque,
            'cor': self.cor,
            'tamanho': self.tamanho,
            'preco': self.preco
        }
    @classmethod
    def buscar_produtos(cls, produto_id):
        produto = cls.query.filter_by(produto_id=produto_id).first()

        if produto:
            return produto
        return False
    
    def salvar_produto(self):
        banco.session.add(self)
        banco.session.commit()

    def atualizar_produto(self, genero, secao, categoria, estilo, nome, descricao, qtd_estoque, cor, tamanho, preco ):
        self.genero = genero
        self.secao = secao
        self.categoria = categoria
        self.estilo = estilo
        self.nome = nome
        self.descricao = descricao
        self.qtd_estoque = qtd_estoque
        self.cor = cor
        self.tamanho = tamanho
        self.preco = preco

    def deletar_produto(self):
        banco.session.delete(self)
        banco.session.commit()