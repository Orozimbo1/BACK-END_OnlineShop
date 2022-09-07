from sql_alquemy import banco

class LojaModel(banco.Model):
    __tablename__ = 'lojas'

    loja_id = banco.Column(banco.String, primary_key=True)
    nome_fantasia = banco.Column(banco.String(40))
    email = banco.Column (banco.String(100))
    senha = banco.Column(banco.String(40))
    CNPJ = banco.Column(banco.String(20))
    telefone = banco.Column(banco.String(20))
    CEP = banco.Column(banco.String(10))
    cidade = banco.Column(banco.String(40)) 
    logradouro = banco.Column(banco.String(40))
    rua = banco.Column(banco.String(80))
    numero = banco.Column(banco.Integer)

    def __init__(self,  loja_id, nome_fantasia, email, senha, CNPJ, telefone, CEP, cidade, logradouro, rua, numero):
        self.loja_id = loja_id
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
            'numero': self.numero
        }
    @classmethod
    def buscar_lojas(cls, nome_fantasia):
        loja = cls.query.filter_by(nome_fantasia=nome_fantasia).first()

        if loja:
            return loja
        return False

    
    def salvar_loja(self):
        banco.session.add(self)
        banco.session.commit()

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
        banco.session.delete(self)
        banco.session.commit()