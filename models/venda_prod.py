from database import Base, engine, session
from sqlalchemy import Column, Integer, ForeignKey, Float
from models.venda import VendaModel
from models.produto import ProdutoModel

class VendaProdModel(Base):
    __tablename__ = 'venda_prod'

    venda_prod_id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey(ProdutoModel.produto_id))
    qtd_produtos = Column(Integer)
    total = Column(Float(2))
    venda_id = Column(Integer, ForeignKey(VendaModel.venda_id))

    def __init__(self, produto_id, venda_id, qtd_produtos, total):
        self.produto_id = produto_id
        self.venda_id = venda_id
        self.qtd_produtos = qtd_produtos
        self.total = total

    def json(self):
        return {
            'venda_prod_id': self.venda_prod_id,
            'produto_id': self.produto_id,
            'qtd_produtos': self.qtd_produtos,
            'total': self.total,
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