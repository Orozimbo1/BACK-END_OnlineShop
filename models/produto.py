from sql_alquemy import Base, engine, session
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.loja import LojaModel
from models.produto_atributos.secao import SecaoProdutoModel
from models.produto_atributos.genero import GeneroProdutoModel
from models.produto_atributos.categoria import CategoriaProdutoModel
from models.produto_atributos.estilo import EstiloProdutoModel


class ProdutoModel(Base):
    __tablename__ = 'produtos' 

    produto_id = Column(Integer, primary_key=True)
    imagens_produto = relationship('ImagemProdutoModel', backref="produtos")
    genero_produto_id = Column(Integer, ForeignKey(GeneroProdutoModel.genero_produto_id))
    secao_produto_id = Column(Integer, ForeignKey(SecaoProdutoModel.secao_produto_id))
    categoria_produto_id = Column(Integer, ForeignKey(CategoriaProdutoModel.categoria_produto_id))
    estilo_produto_id = Column(Integer, ForeignKey(EstiloProdutoModel.estilo_produto_id))
    nome = Column(String(255))
    descricao = Column(String(600))
    qtd_estoque = Column(Integer)
    cor_produto = Column(String(255))
    tamanho_produto = Column(String(255))
    valor = Column(Float(precision=2))
    loja_id = Column(Integer, ForeignKey(LojaModel.loja_id))

    def __init__(self,loja_id,genero_produto_id,secao_produto_id,categoria_produto_id,estilo_produto_id,nome, descricao,qtd_estoque,cor_produto,tamanho_produto,valor):
        self.genero_produto_id = genero_produto_id
        self.secao_produto_id = secao_produto_id
        self.categoria_produto_id = categoria_produto_id
        self.estilo_produto_id = estilo_produto_id
        self.nome = nome
        self.descricao = descricao
        self.qtd_estoque = qtd_estoque
        self.cor_produto = cor_produto
        self.tamanho_produto = tamanho_produto
        self.valor = valor
        self.loja_id = loja_id
    
    def json(self):
        return {
            'loja_id': self.loja_id,
            'produto_id': self.produto_id,
            'imagens_produto': [imagem.json() for imagem in self.imagens_produto],
            'genero_produto_id': self.genero_produto_id,
            'secao_produto_id': self.secao_produto_id,
            'categoria_produto_id': self.categoria_produto_id,
            'estilo_produto_id': self.estilo_produto_id,
            'nome': self.nome,
            'descricao': self.descricao,
            'qtd_estoque': self.qtd_estoque,
            'cor_produto': self.cor_produto,
            'tamanho_produto':self.tamanho_produto,
            'valor': self.valor
        }

    @classmethod
    def buscar_produtos_filtro(cls, genero_produto_id):
        resultado = session.query(ProdutoModel).filter_by(genero_produto_id=genero_produto_id)
        produtos = [produto.json() for produto in resultado]
        return produtos

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

    def atualizar_qtd_produto(self, qtd_estoque):
        self.qtd_estoque = qtd_estoque

    def atualizar_produto(self,loja_id,genero_produto_id,secao_produto_id,categoria_produto_id,estilo_produto_id,nome, descricao,qtd_estoque,cor_produto,tamanho_produto,valor):
        self.genero_produto_id = genero_produto_id
        self.secao_produto_id = secao_produto_id
        self.categoria_produto_id = categoria_produto_id
        self.estilo_produto_id = estilo_produto_id
        self.nome = nome
        self.descricao = descricao
        self.qtd_estoque = qtd_estoque
        self.cor_produto = cor_produto
        self.tamanho_produto = tamanho_produto
        self.valor = valor
        self.loja_id = loja_id

    def deletar_produto(self):
        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)