from sql_alquemy import Base, engine, session
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class VendaModel(Base):
    __tablename__ = 'vendas'

    venda_id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey("produtos.produto_id"))
    produto = relationship("ProdutoModel", backref="vendas")

    def __init__(self, produto_id):
        self.produto_id = produto_id
        
        
    
    def json(self):
        return {
            'venda_id': self.venda_id,
            'produto_id': self.produto_id
            
        }

    @classmethod
    def buscar_todas_vendas(cls):
        resultado = session.query(VendaModel).all()
        vendas = [venda.json() for venda in resultado]
        return vendas
    
    @classmethod
    def buscar_vendas(cls, venda_id):
        venda = session.query(VendaModel).filter_by(venda_id=venda_id).first()

        if venda:
            return venda
        return False

    
    def salvar_venda(self):
        session.add(self)
        session.commit()

    def deletar_venda(self):

        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)