from sql_alquemy import Base, engine, session
from sqlalchemy import Column, String, Integer

class CepLojaModel(Base):
    __tablename__ = 'endereco_lojas'

    endereco_loja_id = Column(Integer, primary_key=True)
    local_endereco = Column(String(255))
    CEP = Column(String(10))
    cidade = Column(String(40)) 
    logradouro = Column(String(40))
    rua = Column(String(80))
    numero = Column(Integer)

    def __init__(self,local_endereco, CEP, cidade, logradouro, rua, numero):
        self.local_endereco = local_endereco
        self.CEP = CEP
        self.cidade = cidade
        self.logradouro = logradouro
        self.rua = rua
        self.numero = numero
        
    
    def json(self):
        return {
            'endereco_loja_id': self.loja_id,
            'local_endereco': self.local_endereco,
            'CEP': self.CEP,
            'cidade': self.cidade,
            'logradouro': self.logradouro,
            'rua': self.rua,
            'numero': self.numero
        }

    @classmethod
    def buscar_todos_enderecos(cls):
        resultado = session.query(CepLojaModel).all()
        enderecos = [endereco.json() for endereco in resultado]
        return enderecos
    
    @classmethod
    def buscar_endereco_por_id(cls, endereco_loja_id):
        endereco = session.query(CepLojaModel).filter_by(endereco_loja_id=endereco_loja_id).first()

        if endereco:
            return endereco
        return False

    def atualizar_endereco(self, local_endereco, CEP, cidade, logradouro, rua, numero):
        self.local_endereco = local_endereco
        self.CEP = CEP
        self.cidade = cidade
        self.logradouro = logradouro
        self.rua = rua
        self.numero = numero  
        
    def salvar_endereco(self):
        session.add(self)
        session.commit()

    def deletar_endereco(self):

        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)