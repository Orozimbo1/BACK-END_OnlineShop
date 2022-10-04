from tokenize import String
from sql_alquemy import Base, engine, session
from sqlalchemy import Column, Integer, String, Float

class PagamentoModel(Base):
    __tablename__ = 'pagamentos'

    pagamento_id = Column(Integer, primary_key=True)
    forma_pagamento = Column(String(100))
    desconto = Column(Integer)

    def __init__(self, forma_pagamento, desconto):
        self.forma_pagamento = forma_pagamento
        self.desconto = desconto

    def json(self):
        return {
            'pagamento_id': self.pagamento_id,
            'forma_pagamento': self.forma_pagamento,
            'desconto': self.desconto
        }

    @classmethod
    def buscar_todos_pagamentos(cls):
        resultado = session.query(PagamentoModel).all()
        pagamentos = [secao.json() for secao in resultado]
        return pagamentos

    @classmethod
    def buscar_pagamento(cls, pagamento_id):
        pagamento = session.query(PagamentoModel).filter_by(pagamento_id=pagamento_id).first()

        if pagamento:
            return pagamento
        return False

    def atualizar_pagamento(self, forma_pagamento, desconto):
        self.forma_pagamento = forma_pagamento
        self.desconto = desconto
    
    def salvar_pagamento(self):
        session.add(self)
        session.commit()

    def deletar_pagamento(self):
        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)