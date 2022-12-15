from database import Base, engine, session
from sqlalchemy import Column, String, Integer, ForeignKey
from models.loja import LojaModel

class ContatoLojaModel(Base):
    __tablename__ = 'contato_lojas'

    contato_loja_id = Column(Integer, primary_key=True)
    loja_id = Column(Integer, ForeignKey(LojaModel.loja_id))
    celular = Column(String(40))
    nome = Column(String(40))

    def __init__(self, loja_id, celular, nome):
        self.loja_id = loja_id
        self.celular = celular
        self.nome = nome
        
        
    
    def json(self):
        return {
            'contato_loja_id': self.contato_loja_id,
            'loja_id': self.loja_id,
            'celular': self.celular,
            'nome': self.nome
        }

    @classmethod
    def buscar_todos_contatos(cls):
        resultado = session.query(ContatoLojaModel).all()
        contatos = [contato.json() for contato in resultado]
        return contatos
    
    @classmethod
    def buscar_contato_por_id(cls, contato_loja_id):
        contato = session.query(ContatoLojaModel).filter_by(contato_loja_id=contato_loja_id).first()

        if contato:
            return contato
        return False

    def atualizar_contato(self, loja_id, celular,nome):
        self.loja_id = loja_id
        self.celular = celular
        self.nome = nome

    def salvar_contato(self):
        session.add(self)
        session.commit()

    def deletar_contato(self):

        session.delete(self)
        session.commit()

Base.metadata.create_all(engine)