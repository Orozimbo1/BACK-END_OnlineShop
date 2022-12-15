from database import Base, engine, session
from sqlalchemy import Column, String, Integer, ForeignKey
from models.loja import LojaModel

class CepLojaModel(Base):
    __tablename__ = 'endereco_lojas'

    endereco_loja_id = Column(Integer, primary_key=True)
    loja_id = Column(Integer, ForeignKey(LojaModel.loja_id))
    CEP = Column(String(10))
    UF = Column(String(10))
    cidade = Column(String(40)) 
    bairro = Column(String(40))
    rua = Column(String(80))
    numero = Column(Integer)

    def __init__(self, loja_id, CEP, UF, cidade, bairro, rua, numero):
        self.loja_id = loja_id
        self.CEP = CEP
        self.UF = UF,
        self.cidade = cidade
        self.bairro = bairro
        self.rua = rua
        self.numero = numero
        
    
    def json(self):
        return {
            'endereco_loja_id': self.endereco_loja_id,
            'loja_id': self.loja_id,
            'CEP': self.CEP,
            'UF': self.UF,
            'cidade': self.cidade,
            'bairro': self.bairro,
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


    def atualizar_endereco(self, local_endereco, CEP, cidade, bairro, rua, numero):
        self.local_endereco = local_endereco

    def atualizar_endereco(self, loja_id, CEP, UF, cidade, bairro, rua, numero):
        self.loja_id = loja_id
        self.CEP = CEP
        self.UF = UF,
        self.cidade = cidade
        self.bairro = bairro
        self.rua = rua
        self.numero = numero
        
    def salvar_endereco(self):
        session.add(self)
        session.commit()

    def deletar_endereco(self):

        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)