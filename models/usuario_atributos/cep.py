from database import Base, engine, session
from sqlalchemy import Column, String, Integer

class CepUsuarioModel(Base):
    __tablename__ = 'endereco_usuarios'

    endereco_usuario_id = Column(Integer, primary_key=True)
    ponto_referencia = Column(String(255))
    CEP = Column(String(10))
    UF = Column(String(10))
    cidade = Column(String(40)) 
    bairro = Column(String(40))
    rua = Column(String(80))
    numero = Column(Integer)

    def __init__(self, ponto_referencia, CEP, UF, cidade, bairro, rua, numero):
        self.ponto_referencia = ponto_referencia
        self.CEP = CEP
        self.UF = UF
        self.cidade = cidade
        self.bairro = bairro
        self.rua = rua
        self.numero = numero
        
    
    def json(self):
        return {
            'endereco_usuario_id': self.endereco_usuario_id,
            'ponto_referencia': self.ponto_referencia,
            'CEP': self.CEP,
            'UF': self.UF,
            'cidade': self.cidade,
            'bairro': self.bairro,
            'rua': self.rua,
            'numero': self.numero
        }

    @classmethod
    def buscar_todos_enderecos(cls):
        resultado = session.query(CepUsuarioModel).all()
        enderecos = [endereco.json() for endereco in resultado]
        return enderecos
    
    @classmethod
    def buscar_endereco_por_id(cls, endereco_usuario_id):
        endereco = session.query(CepUsuarioModel).filter_by(endereco_usuario_id=endereco_usuario_id).first()

        if endereco:
            return endereco
        return False

    def atualizar_endereco(self, ponto_referencia, CEP, UF, cidade, bairro, rua, numero):
        self.ponto_referencia = ponto_referencia
        self.CEP = CEP
        self.UF = UF
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