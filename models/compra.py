from sql_alquemy import Base, engine, session
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class CompraModel(Base):
    __tablename__ = 'compras'

    compra_id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"))
    usuario = relationship("UsuarioModel", backref="compras")
    produto_id = Column(Integer, ForeignKey("produtos.produto_id"))
    produto = relationship("ProdutoModel", backref="vendas")

    def __init__(self, usuario_id, produto_id):
        self.usuario_id = usuario_id
        self.produto_id = produto_id
    
    def json(self):
        return {
            'venda_id': self.venda_id,
            'usuario_id': self.usuario_id,
            'produto_id': self.produto_id
        }

    @classmethod
    def buscar_todas_compras(cls):
        resultado = session.query(CompraModel).all()
        compras = [venda.json() for venda in resultado]
        return compras
    
    @classmethod
    def buscar_compras(cls, compra_id):
        compra = session.query(CompraModel).filter_by(compra_id=compra_id).first()

        if compra:
            return compra
        return False

    
    def salvar_compra(self):
        session.add(self)
        session.commit()

    def deletar_compra(self):

        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)