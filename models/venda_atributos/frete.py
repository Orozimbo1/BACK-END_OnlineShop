from tokenize import String
from sql_alquemy import Base, engine, session
from sqlalchemy import Column, Integer, String, Float

class FreteModel(Base):
    __tablename__ = 'fretes'

    frete_id = Column(Integer, primary_key=True)
    prazo_entrega = Column(String(100))
    valor_frete = Column(Float(2))

    def __init__(self, prazo_entrega, valor_frete):
        self.prazo_entrega = prazo_entrega
        self.valor_frete = valor_frete

    def json(self):
        return {
            'frete_id': self.frete_id,
            'prazo_entrega': self.prazo_entrega,
            'valor_frete': self.valor_frete
        }

    @classmethod
    def buscar_todos_fretes(cls):
        resultado = session.query(FreteModel).all()
        fretes = [secao.json() for secao in resultado]
        return fretes

    @classmethod
    def buscar_frete(cls, frete_id):
        frete = session.query(FreteModel).filter_by(frete_id=frete_id).first()

        if frete:
            return frete
        return False

    def atualizar_frete(self, prazo_entrega, valor_frete):
        self.prazo_entrega = prazo_entrega
        self.valor_frete = valor_frete
    
    def salvar_frete(self):
        session.add(self)
        session.commit()

    def deletar_frete(self):
        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)