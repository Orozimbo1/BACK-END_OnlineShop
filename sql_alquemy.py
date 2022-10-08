import sqlalchemy
import dotenv
import os
from sqlalchemy.orm import declarative_base, sessionmaker

dotenv.load_dotenv(dotenv.find_dotenv())

engine = sqlalchemy.create_engine(os.getenv("DATABASE_URL"))
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()