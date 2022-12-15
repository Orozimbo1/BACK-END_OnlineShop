from tokenize import String
from database import Base, engine, session
from sqlalchemy import Column, Integer, String

class EstiloProdutoModel(Base):
    __tablename__ = 'estilo_produtos'

    estilo_produto_id = Column(Integer, primary_key=True)
    nome_estilo = Column(String(100))

    def __init__(self, nome_estilo):
        self.nome_estilo = nome_estilo

    def json(self):
        return {
            'estilo_produto_id': self.estilo_produto_id,
            'nome_estilo': self.nome_estilo
        }

    @classmethod
    def buscar_todos_estilos(cls):
        resultado = session.query(EstiloProdutoModel).all()
        estilos = [estilo.json() for estilo in resultado]
        return estilos

    @classmethod
    def buscar_estilo(cls, estilo_produto_id):
        estilo = session.query(EstiloProdutoModel).filter_by(estilo_produto_id=estilo_produto_id).first()

        if estilo:
            return estilo
        return False
    
    def salvar_estilo(self):
        session.add(self)
        session.commit()

    def deletar_estilo(self):
        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)