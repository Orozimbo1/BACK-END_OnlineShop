from sql_alquemy import Base, engine, session
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class UsuarioModel(Base):
    __tablename__ = 'usuarios'

    usuario_id = Column(Integer, primary_key=True)
    nome = Column(String(80))
    sobrenome = Column(String(80))
    email = Column(String(40))
    senha = Column(String(40))
    telefone = Column(String(20))
    CPF = Column(String(13))
    CEP = Column(String(10))
    cidade = Column(String(80))
    logradouro = Column(String(80))
    rua = Column(String(80))
    numero = Column(Integer)
    compras = relationship('CompraModel', backref="usuarios")
    

    def __init__(self, nome, sobrenome, email, senha, telefone, CPF, CEP, cidade, logradouro, rua, numero):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.CPF = CPF
        self.CEP = CEP
        self.cidade = cidade
        self.logradouro = logradouro
        self.rua = rua
        self.numero = numero
    
    def json(self):
        return {
            'usuario_id': self.usuario_id,
            'nome': self.nome,
            'sobrenome': self.sobrenome,
            'email': self.email,
            'telefone': self.telefone,
            'CPF': self.CPF,
            'CEP': self.CEP,
            'cidade': self.cidade,
            'logradouro': self.logradouro,
            'rua': self.rua,
            'numero': self.numero,
            'compras': [compra.json() for compra in self.compras]
        }
    
    def jsonLogin(self):
        return {
            'usuario_id': self.usuario_id,
            'email': self.email
        }

    @classmethod
    def buscar_todos_usuarios(cls):
        resultado = session.query(UsuarioModel).all()
        usuarios = [usuario.json() for usuario in resultado]
        return usuarios

    @classmethod
    def buscar_usuario(cls, usuario_id):
        usuario = session.query(UsuarioModel).filter_by(usuario_id=usuario_id).first()

        if usuario:
            return usuario
        return None

    @classmethod
    def buscar_email_usuario(cls, email):
        usuario = session.query(UsuarioModel).filter_by(email=email).first()

        if usuario:
            return usuario
        return None

    def salvar_usuario(self):

        session.add(self)
        session.commit()

    def atualizar_usuario(self, nome, sobrenome, email, senha, telefone, CPF, CEP, cidade, logradouro, rua, numero):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.CPF = CPF
        self.CEP = CEP
        self.cidade = cidade
        self.logradouro = logradouro
        self.rua = rua
        self.numero = numero

    def deletar_usuario(self):
        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)
