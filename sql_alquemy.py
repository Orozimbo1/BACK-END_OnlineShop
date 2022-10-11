import sqlalchemy
import dotenv
import os
from sqlalchemy.orm import declarative_base, sessionmaker


dotenv.load_dotenv(dotenv.find_dotenv())

engine = sqlalchemy.create_engine("postgresql://fbweefymqxihya:83e3c84c8d71837369dfb8aedc40a39aad0a00e73011e5b43e380e4f094803ab@ec2-44-210-228-110.compute-1.amazonaws.com:5432/d3i3329k5l69u8")
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()