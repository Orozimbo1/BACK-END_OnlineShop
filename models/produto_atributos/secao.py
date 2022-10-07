from tokenize import String
from sql_alquemy import Base, engine, session
from sqlalchemy import Column, Integer, String

class SecaoProdutoModel(Base):
    __tablename__ = 'secao_produtos'

    secao_produto_id = Column(Integer, primary_key=True)
    nome_secao = Column(String(100))

    def __init__(self, nome_secao):
        self.nome_secao = nome_secao

    def json(self):
        return {
            'secao_produto_id': self.secao_produto_id,
            'nome_secao': self.nome_secao
        }

    @classmethod
    def buscar_todas_secoes(cls):
        resultado = session.query(SecaoProdutoModel).all()
        secaos = [secao.json() for secao in resultado]
        return secaos

    @classmethod
    def buscar_secao(cls, secao_produto_id):
        secao = session.query(SecaoProdutoModel).filter_by(secao_produto_id=secao_produto_id).first()

        if secao:
            return secao
        return False
    
    def salvar_secao(self):
        session.add(self)
        session.commit()

    def deletar_secao(self):
        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)