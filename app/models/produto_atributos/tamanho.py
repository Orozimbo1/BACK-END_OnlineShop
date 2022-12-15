from tokenize import String
from database import Base, engine, session
from sqlalchemy import Column, Integer, String, ForeignKey
from models.produto import ProdutoModel

class TamanhoProdutoModel(Base):
    __tablename__ = 'tamanho_produtos'

    tamanho_produto_id = Column(Integer, primary_key=True)
    nome_tamanho = Column(String(100))
    produto_id = Column(Integer, ForeignKey(ProdutoModel.produto_id))

    def __init__(self, nome_tamanho, produto_id):
        self.nome_tamanho = nome_tamanho
        self.produto_id = produto_id

    def json(self):
        return {
            'tamanho_produto_id': self.tamanho_produto_id,
            'nome_tamanho': self.nome_tamanho,
            'produto_id': self.produto_id
        }

    @classmethod
    def buscar_todos_tamanhos(cls):
        resultado = session.query(TamanhoProdutoModel).all()
        tamanhos = [tamanho.json() for tamanho in resultado]
        return tamanhos

    @classmethod
    def buscar_tamanho(cls, tamanho_produto_id):
        tamanho = session.query(TamanhoProdutoModel).filter_by(tamanho_produto_id=tamanho_produto_id).first()

        if tamanho:
            return tamanho
        return False
    
    def salvar_tamanho(self):
        session.add(self)
        session.commit()

    def deletar_tamanho(self):
        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)