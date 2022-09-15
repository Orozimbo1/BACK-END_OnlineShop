import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker

engine = sqlalchemy.create_engine('postgresql://postgres:postgres@localhost/OnlineShop')
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()