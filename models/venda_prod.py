from sql_alquemy import Base, engine, session
from sqlalchemy import Column, Integer, ForeignKey
from models.venda import VendaModel

class VendaProdModel(Base):
    __tablename__ = 'venda_prod'

    venda_prod_id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey("produtos.produto_id"))
    venda_id = Column(Integer, ForeignKey("vendas.venda_id"))

    def __init__(self, produto_id, venda_id):
        self.produto_id = produto_id
        self.venda_id = venda_id

    def json(self):
        return {
            'venda_prod_id': self.venda_prod_id,
            'produto_id': self.produto_id,
            'venda_id': self.venda_id
        }

    @classmethod
    def buscar_todas_vendas_prod(cls):
        resultado = session.query(VendaProdModel).all()
        vendas = [venda.json() for venda in resultado]
        return vendas

    @classmethod
    def buscar_venda_prod(cls, venda_prod_id):
        venda_prod = session.query(VendaProdModel).filter_by(venda_prod_id=venda_prod_id).first()

        if venda_prod:
            return venda_prod
        return False
    
    def salvar_venda_prod(self):
        session.add(self)
        session.commit()

    def deletar_venda_prod(self):
        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)