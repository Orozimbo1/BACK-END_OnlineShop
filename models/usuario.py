from sql_alquemy import banco

class UsuarioModel(banco.Model):
    __tablename__ = 'usuarios'

    usuario_id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(80))
    sobrenome = banco.Column(banco.String(80))
    email = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))
    telefone = banco.Column(banco.String(20))
    CPF = banco.Column(banco.String(13))
    CEP = banco.Column(banco.String(10))
    cidade = banco.Column(banco.String(80))
    logradouro = banco.Column(banco.String(80))
    rua = banco.Column(banco.String(80))
    numero = banco.Column(banco.Integer)
    

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
            'numero': self.numero
        }
    
    def jsonLogin(self):
        return {
            'usuario_id': self.usuario_id,
            'email': self.email
        }


    @classmethod
    def buscar_usuario(cls, usuario_id):
        usuario = cls.query.filter_by(usuario_id=usuario_id).first()

        if usuario:
            return usuario
        return None
    
    @classmethod
    def buscar_email_usuario(cls, email):
        usuario = cls.query.filter_by(email=email).first()

        if usuario:
            return usuario
        return None

    def salvar_usuario(self):

        banco.session.add(self)
        banco.session.commit()

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
        banco.session.delete(self)
        banco.session.commit()
