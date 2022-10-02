from tokenize import String
from sql_alquemy import Base, engine, session
from sqlalchemy import Column, Integer

class QtdProdutoModel(Base):
    __tablename__ = 'qtd_produtos'

    qtd_produto_id = Column(Integer, primary_key=True)
    qtd_produto = Column(Integer)

    def __init__(self, nome_qtd):
        self.nome_qtd = nome_qtd

    def json(self):
        return {
            'qtd_produto_id': self.qtd_produto_id,
            'qtd_produto': self.qtd_produto
        }

    @classmethod
    def buscar_todas_qtds(cls):
        resultado = session.query(QtdProdutoModel).all()
        qtds = [qtd.json() for qtd in resultado]
        return qtds

    @classmethod
    def buscar_qtd(cls, qtd_produto_id):
        qtd = session.query(QtdProdutoModel).filter_by(qtd_produto_id=qtd_produto_id).first()

        if qtd:
            return qtd
        return False
    
    def atualizar_qtd(self, qtd_produto):
        self.qtd_produto = qtd_produto
    
    def salvar_qtd(self):
        session.add(self)
        session.commit()

    def deletar_qtd(self):
        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)