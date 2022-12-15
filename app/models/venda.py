from database import Base, engine, session
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Float, String
from sqlalchemy.orm import relationship
from models.venda_atributos.pagamento import PagamentoModel
from models.venda_atributos.frete import FreteModel

class VendaModel(Base):
    __tablename__ = 'vendas'

    venda_id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"))
    pagamento_id = Column(Integer, ForeignKey(PagamentoModel.pagamento_id))
    frete_id = Column(Integer, ForeignKey(FreteModel.frete_id))
    total = Column(Float(2))
    total_pago = Column(Float(2))
    data = Column(TIMESTAMP)
    produtos = relationship('VendaProdModel', backref='vendas')

    def __init__(self, usuario_id, pagamento_id, frete_id, total, total_pago, data):
        self.usuario_id = usuario_id
        self.pagamento_id = pagamento_id
        self.frete_id = frete_id
        self.total = total
        self.total_pago = total_pago
        self.data = data

    def json(self):
        return {
            'venda_id': self.venda_id,
            'usuario_id': self.usuario_id,
            'pagamento_id': self.pagamento_id,
            'frete_id': self.frete_id,
            'total': self.total,
            'total_pago': self.total_pago,
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