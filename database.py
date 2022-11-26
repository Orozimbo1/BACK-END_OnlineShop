import sqlalchemy
# import dotenv
# import os
from sqlalchemy.orm import declarative_base, sessionmaker

# dotenv.load_dotenv(dotenv.find_dotenv())

engine = sqlalchemy.create_engine('postgresql://{}:{}@{}:{}/{}'.format(os.getenv("USUARIO"),os.getenv("SENHA"),os.getenv("HOST"),os.getenv("PORTA"),os.getenv("DB")))
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


# connection = psycopg2.connect(
#     host ="onlineshop.cgvog13pctzv.us-east-1.rds.amazonaws.com",
#     port= 5432,
#     user="postgres",
#     password="postgres",
#     database="onlineshop"
# )

# connection.autocommit=True

# cursor = connection.cursor()

# connection.close()