import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, Integer

engine = sqlalchemy.create_engine('postgresql://postgres:postgres@localhost/OnlineShop')
Base = declarative_base()

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

Base.metadata.create_all(engine)

usuario = UsuarioModel(nome='matheus', sobrenome='matheus', email='matheus', senha='matheus', telefone='123', CPF='123', CEP='123', cidade='matheus', logradouro='matheus', rua='matheus', numero=123)

Session = sessionmaker(bind=engine)
session = Session()
session.add(usuario)
session.commit()

usuario_encontrado = session.query(UsuarioModel).filter_by(nome='matheus').first()
print('#################')
print(usuario_encontrado)
print('#################')

# import psycopg2

# connection = psycopg2.connect(host="localhost", dbname="OnlineShop", user="postgres", password="postgres")
# cursor = connection.cursor()

# print('conexão estabeecida')

# cursor.execute("CREATE TABLE aulas(id bigserial PRIMARY KEY, name varchar)")
# connection.commit()


# def normalizar_caminho_parametros(genero=None,
#                             secao=None,
#                             categoria=None,
#                             estilo=None,
#                             cor=None,
#                             tamanho=None,
#                             preco_min= 0,
#                             preco_max = 20000,
#                             limit = 10,
#                             offset = 0, **dados):
    # if genero:
    #     return{ 
    #             genero: genero,
                # secao: secao,
                # categoria: categoria,
                # estilo: estilo,
                # cor: cor,
                # tamanho: tamanho,
        #         preco_min: preco_min,
        #         preco_max: preco_max,
        #         limit: limit,
        #         offset: offset
        # }

    # return  {   
                # secao: secao,
                # categoria: categoria,
                # estilo: estilo,
                # cor: cor,
                # tamanho: tamanho,
            #     preco_min: preco_min,
            #     preco_max: preco_max,
            #     limit: limit,
            #     offset: offset
            # }

# caminho_parametros = reqparse.RequestParser()
# caminho_parametros.add_argument('genero', type=str)
# caminho_parametros.add_argument('secao', type=str)
# caminho_parametros.add_argument('categoria', type=str)
# caminho_parametros.add_argument('estilo', type=str)
# caminho_parametros.add_argument('nome', type=str)
# caminho_parametros.add_argument('cor', type=str)
# caminho_parametros.add_argument('tamanho', type=str)
# caminho_parametros.add_argument('preco_min', type=float)
# caminho_parametros.add_argument('preco_max', type=float)
# caminho_parametros.add_argument('limit', type=float)
# caminho_parametros.add_argument('offset', type=float)



# connection = sqlite3.connect('banco.db')
        # cursor = connection.cursor()

        # dados = caminho_parametros.parse_args()
        # dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        # parametros = normalizar_caminho_parametros(**dados_validos)
        
        # if not parametros.get('genero'):
        #     consulta = "SELECT * FROM produtos WHERE (preco >= ? or preco <= ?) LIMIT ? OFFSET ?"
        #     tupla = tuple([parametros[chave] for chave in parametros])
        #     resultado = cursor.execute(consulta, tupla)
        # else:
        #     consulta = "SELECT * FROM produtos WHERE (preco > ? or preco < ?) or genero = ?  LIMIT ? OFFSET ?"
        #     tupla = tuple([parametros[chave] for chave in parametros])
        #     resultado = cursor.execute(consulta, tupla)
        
        # produtos = []
        # for linha in resultado:
        #     produtos.append({
        #             "produto_id" : linha[0],
        #             "genero" : linha[1],
        #             "secao" : linha [2],
        #             "categoria" : linha[3],
        #             "estilo" : linha[4],
        #             "nome": linha[5],
        #             "descricao" :linha[6],
        #             "qtd_estoque" : linha[7],
        #             "cor" : linha[8],
        #             "tamanho" : linha[9],
        #             "preco" : linha[10]
        #             })

        # return {"produtos": produtos}