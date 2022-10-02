from tokenize import String
from sql_alquemy import Base, engine, session
from sqlalchemy import Column, Integer, String

class CorProdutoModel(Base):
    __tablename__ = 'cor_produtos'

    cor_produto_id = Column(Integer, primary_key=True)
    nome_cor = Column(String(100))

    def __init__(self, nome_cor):
        self.nome_cor = nome_cor

    def json(self):
        return {
            'cor_produto_id': self.cor_produto_id,
            'nome_cor': self.nome_cor
        }

    @classmethod
    def buscar_todas_cores(cls):
        resultado = session.query(CorProdutoModel).all()
        cores = [cor.json() for cor in resultado]
        return cores

    @classmethod
    def buscar_cor(cls, cor_produto_id):
        cor = session.query(CorProdutoModel).filter_by(cor_produto_id=cor_produto_id).first()

        if cor:
            return cor
        return False
    
    def salvar_cor(self):
        session.add(self)
        session.commit()

    def deletar_cor(self):
        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)