import sqlalchemy
import dotenv
import os
from sqlalchemy.orm import declarative_base, sessionmaker

dotenv.load_dotenv(dotenv.find_dotenv())

engine = sqlalchemy.create_engine('postgresql://{}:{}@{}:{}/{}'.format(os.getenv("usuario"),os.getenv("senha"),os.getenv("host"),os.getenv("port"), os.getenv("db")))
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()