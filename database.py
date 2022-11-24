import sqlalchemy
import dotenv
import os
from sqlalchemy.orm import declarative_base, sessionmaker

dotenv.load_dotenv(dotenv.find_dotenv())

engine = sqlalchemy.create_engine('postgresql://{}:{}@{}:{}/{}'.format(os.getenv("USUARIO"),os.getenv("SENHA"),os.getenv("HOST"),os.getenv("PORTA"),os.getenv("DB")))
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()