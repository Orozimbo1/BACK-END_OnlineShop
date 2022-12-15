from database import Base, engine, session
from sqlalchemy import Column, String, Integer, ForeignKey
from models.usuario import UsuarioModel

class ContatoUsuarioModel(Base):
    __tablename__ = 'contato_usuarios'

    contato_usuario_id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey(UsuarioModel.usuario_id))
    celular = Column(String(40))
    nome = Column(String(40))

    def __init__(self, usuario_id, celular, nome):
        self.usuario_id = usuario_id
        self.celular = celular
        self.nome = nome
        
        
    
    def json(self):
        return {
            'contato_usuario_id': self.contato_usuario_id,
            'usuario_id': self.usuario_id,
            'celular': self.celular,
            'nome': self.nome,
        }

    @classmethod
    def buscar_todos_contatos(cls):
        resultado = session.query(ContatoUsuarioModel).all()
        contatos = [contato.json() for contato in resultado]
        return contatos
    
    @classmethod
    def buscar_contato_por_id(cls, contato_usuario_id):
        contato = session.query(ContatoUsuarioModel).filter_by(contato_usuario_id=contato_usuario_id).first()

        if contato:
            return contato
        return False

    def atualizar_contato(self, usuario_id, celular, nome):
        self.usuario_id = usuario_id
        self.celular = celular
        self.nome = nome

    def salvar_contato(self):
        
        session.add(self)
        session.commit()

    def deletar_contato(self):

        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)