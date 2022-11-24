from database import Base, engine, session
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash
from models.usuario_atributos.contato import ContatoUsuarioModel
from models.usuario_atributos.cep import CepUsuarioModel


class UsuarioModel(Base):
    __tablename__ = 'usuarios'

    usuario_id = Column(Integer, primary_key=True)
    img_perfil_usuario = Column(String)
    nome = Column(String(80))
    sobrenome = Column(String(80))
    email = Column(String(40))
    senha = Column(String(200))
    CPF = Column(String(13))
    contato_usuario_id = Column(Integer, ForeignKey(ContatoUsuarioModel.contato_usuario_id))
    endereco_usuario_id = Column(Integer, ForeignKey(CepUsuarioModel.endereco_usuario_id))
    compras = relationship('VendaModel', backref="usuarios")
    

    def __init__(self, nome, sobrenome, email, senha, CPF, contato_usuario_id, endereco_usuario_id):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha = senha
        self.CPF = CPF
        self.contato_usuario_id = contato_usuario_id
        self.endereco_usuario_id = endereco_usuario_id
    
    def json(self):
        return {
            'usuario_id': self.usuario_id,
            'img_perfil_usuario': self.img_perfil_usuario,
            'nome': self.nome,
            'sobrenome': self.sobrenome,
            'email': self.email,
            'CPF': self.CPF,
            'contato_usuario_id': self.contato_usuario_id,
            'endereco_usuario_id': self.endereco_usuario_id,
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

    def hash_senha(self, senha):
        hash = generate_password_hash(senha)
        self.senha = hash

    def salvar_usuario(self):
        session.add(self)
        session.commit()

    def atualizar_usuario(self, nome, sobrenome, email, CPF, contato_usuario_id, endereco_usuario_id):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.CPF = CPF
        self.contato_usuario_id = contato_usuario_id
        self.endereco_usuario_id = endereco_usuario_id

    def deletar_usuario(self):
        [compra.deletar_venda() for compra in self.compras]
        
        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)
