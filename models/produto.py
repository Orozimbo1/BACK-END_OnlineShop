from sql_alquemy import Base, engine, session
from sqlalchemy import Column, String, Integer, Float

class ProdutoModel(Base):
    __tablename__ = 'produtos'

    produto_id = Column(Integer, primary_key=True)
    genero = Column(String(255))
    secao = Column(String(255))
    categoria = Column(String(255))
    estilo = Column(String(255))
    nome = Column(String(255))
    descricao = Column(String(600))
    qtd_estoque = Column(Integer)
    cor = Column(String(255))
    tamanho = Column(String(255))
    preco = Column(Float(precision=2))

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
    def buscar_todos_produtos(cls):
        resultado = session.query(ProdutoModel).all()
        produtos = [produto.json() for produto in resultado]
        return produtos

    @classmethod
    def buscar_produtos(cls, produto_id):
        produto = session.query(ProdutoModel).filter_by(produto_id=produto_id).first()

        if produto:
            return produto
        return False
    
    def salvar_produto(self):
        session.add(self)
        session.commit()

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
        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)