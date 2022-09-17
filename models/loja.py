from sql_alquemy import Base, engine, session
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class LojaModel(Base):
    __tablename__ = 'lojas'

    loja_id = Column(Integer, primary_key=True)
    nome_fantasia = Column(String(40))
    email = Column (String(100))
    senha = Column(String(40))
    CNPJ = Column(String(20))
    telefone = Column(String(20))
    CEP = Column(String(10))
    cidade = Column(String(40)) 
    logradouro = Column(String(40))
    rua = Column(String(80))
    numero = Column(Integer)
    produtos = relationship('ProdutoModel', backref="lojas")

    def __init__(self, nome_fantasia, email, senha, CNPJ, telefone, CEP, cidade, logradouro, rua, numero):
        self.nome_fantasia = nome_fantasia
        self.email = email
        self.senha = senha
        self.CNPJ = CNPJ
        self.telefone = telefone
        self.CEP = CEP
        self.cidade = cidade
        self.logradouro = logradouro
        self.rua = rua
        self.numero = numero
        
    
    def json(self):
        return {
            'loja_id': self.loja_id,
            'nome_fantasia': self.nome_fantasia,
            'email': self.email,
            'CNPJ': self.CNPJ,
            'telefone': self.telefone,
            'CEP': self.CEP,
            'cidade': self.cidade,
            'logradouro': self.logradouro,
            'rua': self.rua,
            'numero': self.numero,
            'produtos': [produto.json() for produto in self.produtos]
        }

    @classmethod
    def buscar_todas_lojas(cls):
        resultado = session.query(LojaModel).all()
        lojas = [loja.json() for loja in resultado]
        return lojas

    @classmethod
    def buscar_lojas(cls, nome_fantasia):
        loja = session.query(LojaModel).filter_by(nome_fantasia=nome_fantasia).first()

        if loja:
            return loja
        return False
    
    @classmethod
    def buscar_loja_por_id(cls, loja_id):
        loja = session.query(LojaModel).filter_by(loja_id=loja_id).first()

        if loja:
            return loja
        return False

    
    def salvar_loja(self):
        session.add(self)
        session.commit()

    def atualizar_loja(self, nome_fantasia, email, senha, CNPJ, telefone, CEP, cidade, logradouro, rua, numero):
        self.nome_fantasia = nome_fantasia
        self.email = email
        self.senha = senha
        self.CNPJ = CNPJ
        self.telefone = telefone
        self.CEP = CEP
        self.cidade = cidade
        self.logradouro = logradouro
        self.rua = rua
        self.numero = numero

    def deletar_loja(self):
        [produto.deletar_produto() for produto in self.produtos]

        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)