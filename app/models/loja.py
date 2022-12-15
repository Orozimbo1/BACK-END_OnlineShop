from database import Base, engine, session
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash

class LojaModel(Base):
    __tablename__ = 'lojas'

    loja_id = Column(Integer, primary_key=True)
    img_perfil_loja = Column(String)
    nome_fantasia = Column(String(40))
    email = Column (String(100))
    senha = Column(String(200))
    CNPJ = Column(String(20))
    contatos = relationship('ContatoLojaModel', backref="lojas")
    enderecos = relationship('CepLojaModel', backref="lojas")
    produtos = relationship('ProdutoModel', backref="lojas")

    def __init__(self, img_perfil_loja, nome_fantasia, email, senha, CNPJ):
        self.img_perfil_loja = img_perfil_loja
        self.nome_fantasia = nome_fantasia
        self.email = email
        self.senha = senha
        self.CNPJ = CNPJ 
    
    def json(self):
        return {
            'loja_id': self.loja_id,
            'img_perfil_loja': self.img_perfil_loja,
            'nome_fantasia': self.nome_fantasia,
            'email': self.email,
            'CNPJ': self.CNPJ,
            'contatos': [contato.json() for contato in self.contatos],
            'enderecos': [endereco.json() for endereco in self.enderecos],
            'produtos': [produto.json() for produto in self.produtos]
        }

    @classmethod
    def buscar_todas_lojas(cls):
        resultado = session.query(LojaModel).all()
        lojas = [loja.json() for loja in resultado]
        return lojas

    @classmethod
    def buscar_loja_por_email(cls, email):
        loja= session.query(LojaModel).filter_by(email=email).first()
        if loja:
            return loja
        return False
    
    @classmethod
    def buscar_loja_por_id(cls, loja_id):
        loja = session.query(LojaModel).filter_by(loja_id=loja_id).first()

        if loja:
            return loja
        return False
    
    def hash_senha_loja(self, senha):
        hash = generate_password_hash(senha)
        self.senha = hash

    
    def salvar_loja(self):
        session.add(self)
        session.commit()

    def atualizar_loja(self, img_perfil_loja, nome_fantasia, email, senha, CNPJ):
        self.img_perfil_loja = img_perfil_loja
        self.nome_fantasia = nome_fantasia
        self.email = email
        self.senha = senha
        self.CNPJ = CNPJ 

    def deletar_loja(self):
        [produto.deletar_produto() for produto in self.produtos]

        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)