from sql_alquemy import Base, engine, session
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

class VendaModel(Base):
    __tablename__ = 'vendas'

    venda_id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"))
    data = Column(TIMESTAMP)
    produtos = relationship('VendaProdModel', backref='vendas')

    def __init__(self, usuario_id):
        self.usuario_id = usuario_id

    def json(self):
        return {
            'venda_id': self.venda_id,
            'data': self.data,
            'produtos': [produto.json() for produto in self.produtos]
        }

    @classmethod
    def buscar_todas_vendas(cls):
        resultado = session.query(VendaModel).all()
        vendas = [venda.json() for venda in resultado]
        return vendas

    @classmethod
    def buscar_venda(cls, venda_id):
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