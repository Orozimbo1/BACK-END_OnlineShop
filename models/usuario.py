from sql_alquemy import banco

class UsuarioModel(banco.Model):
    __tablename__ = 'usuarios'

    usuario_id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(80))
    sobrenome = banco.Column(banco.String(80))
    email = banco.Column(banco.String(100))
    senha = banco.Column(banco.String(80))
    telefone = banco.Column(banco.String(20))
    CPF = banco.Column(banco.String(13))
    CEP = banco.Column(banco.String(10))
    cidade = banco.Column(banco.String(40))
    logradouro = banco.Column(banco.String(40))
    rua = banco.Column(banco.String(80))
    numero = banco.Column(banco.Integer)

    def __init__(self, usuario_id, nome, sobrenome, email, senha, telefone, CPF, CEP, cidade, logradouro, rua, numero):
        self.usuario_id = usuario_id
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
            'senha': self.senha,
            'telefone': self.telefone,
            'CPF': self.CPF,
            'CEP': self.CEP,
            'cidade': self.cidade,
            'logradouro': self.logradouro,
            'rua': self.rua,
            'numero': self.numero
        }
