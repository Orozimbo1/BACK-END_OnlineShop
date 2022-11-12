from tokenize import String
from sql_alquemy import Base, engine, session
from sqlalchemy import Column, Integer, String, ForeignKey,update
from models.produto import ProdutoModel

class ImagemProdutoModel(Base):
    __tablename__ = 'imagem_produtos'

    imagem_produto_id = Column(Integer, primary_key=True)
    url_imagem = Column(String(100))
    descricao_imagem = Column(String(200))
    produto_id = Column(Integer, ForeignKey(ProdutoModel.produto_id))

    def __init__(self, url_imagem, descricao_imagem, produto_id):
        self.url_imagem = url_imagem
        self.descricao_imagem = descricao_imagem
        self.produto_id = produto_id

    def json(self):
        return {
            'imagem_produto_id': self.imagem_produto_id,
            'url_imagem': self.url_imagem,
            'descricao_imagem': self.descricao_imagem,
            'produto_id': self.produto_id
        }

    @classmethod
    def buscar_todas_imagens(cls):
        resultado = session.query(ImagemProdutoModel).all()
        imagems = [imagem.json() for imagem in resultado]
        return imagems

    @classmethod
    def buscar_imagem(cls, imagem_produto_id):
        imagem = session.query(ImagemProdutoModel).filter_by(imagem_produto_id=imagem_produto_id).first()

        if imagem:
            return imagem
        return False
    
    def salvar_imagem(self):
        session.add(self)
        session.commit()

    def deletar_imagem(self):
        session.delete(self)
        session.commit()
    
    def atualizar_imagem_produto(self, url_imagem, descricao_imagem, produto_id):
        self.url_imagem = url_imagem
        self.descricao_imagem = descricao_imagem
        self.produto_id = produto_id
    
        
Base.metadata.create_all(engine)