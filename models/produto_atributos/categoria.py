from tokenize import String
from sql_alquemy import Base, engine, session
from sqlalchemy import Column, Integer, String

class CategoriaProdutoModel(Base):
    __tablename__ = 'categoria_produtos'

    categoria_produto_id = Column(Integer, primary_key=True)
    nome_categoria = Column(String(100))

    def __init__(self, nome_categoria):
        self.nome_categoria = nome_categoria

    def json(self):
        return {
            'categoria_produto_id': self.categoria_produto_id,
            'nome_categoria': self.nome_categoria
        }

    @classmethod
    def buscar_todas_categorias(cls):
        resultado = session.query(CategoriaProdutoModel).all()
        categorias = [categoria.json() for categoria in resultado]
        return categorias

    @classmethod
    def buscar_categoria(cls, categoria_produto_id):
        categoria = session.query(CategoriaProdutoModel).filter_by(categoria_produto_id=categoria_produto_id).first()

        if categoria:
            return categoria
        return False
    
    def salvar_categoria(self):
        session.add(self)
        session.commit()

    def deletar_categoria(self):
        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)