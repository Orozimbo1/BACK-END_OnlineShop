from tokenize import String
from database import Base, engine, session
from sqlalchemy import Column, Integer, String

class GeneroProdutoModel(Base):
    __tablename__ = 'genero_produtos'

    genero_produto_id = Column(Integer, primary_key=True)
    nome_genero = Column(String(100))

    def __init__(self, nome_genero):
        self.nome_genero = nome_genero

    def json(self):
        return {
            'genero_produto_id': self.genero_produto_id,
            'nome_genero': self.nome_genero
        }

    @classmethod
    def buscar_todos_generos(cls):
        resultado = session.query(GeneroProdutoModel).all()
        generos = [genero.json() for genero in resultado]
        return generos

    @classmethod
    def buscar_genero(cls, genero_produto_id):
        genero = session.query(GeneroProdutoModel).filter_by(genero_produto_id=genero_produto_id).first()

        if genero:
            return genero
        return False
    
    def salvar_genero(self):
        session.add(self)
        session.commit()

    def deletar_genero(self):
        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)