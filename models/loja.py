from sql_alquemy import Base, engine, session
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash
from models.loja_atributos.contato import ContatoLojaModel
from models.loja_atributos.cep import CepLojaModel

class LojaModel(Base):
    __tablename__ = 'lojas'

    loja_id = Column(Integer, primary_key=True)
    img_perfil_loja = Column(String)
    nome_fantasia = Column(String(40))
    email = Column (String(100))
    senha = Column(String(200))
    CNPJ = Column(String(20))
    contato_loja_id = Column(Integer, ForeignKey(ContatoLojaModel.contato_loja_id))
    endereco_loja_id = Column(Integer, ForeignKey(CepLojaModel.endereco_loja_id))
    produtos = relationship('ProdutoModel', backref="lojas")

    def __init__(self, nome_fantasia, email, senha, CNPJ, contato_loja_id, endereco_loja_id):
        self.nome_fantasia = nome_fantasia
        self.email = email
        self.senha = senha
        self.CNPJ = CNPJ
        self.contato_loja_id = contato_loja_id
        self.endereco_loja_id = endereco_loja_id  
    
    def json(self):
        return {
            'loja_id': self.loja_id,
            'img_perfil_loja': self.img_perfil_loja,
            'nome_fantasia': self.nome_fantasia,
            'email': self.email,
            'CNPJ': self.CNPJ,
            'contato_loja_id': self.contato_loja_id,
            'endereco_loja_id': self.endereco_loja_id
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

    def atualizar_loja(self, nome_fantasia, email, CNPJ, contato_loja_id, endereco_loja_id):
        self.nome_fantasia = nome_fantasia
        self.email = email
        self.CNPJ = CNPJ
        self.contato_loja_id = contato_loja_id
        self.endereco_loja_id = endereco_loja_id

    def deletar_loja(self):
        [produto.deletar_produto() for produto in self.produtos]

        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)