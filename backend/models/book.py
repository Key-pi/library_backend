import os

from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


DB_USER = os.environ.get('POSTGRES_USER', 'username')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'password')
DB_NAME = os.environ.get('POSTGRES_DB', 'dbname')
engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@db/{DB_NAME}"
)
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    date_published = Column(DateTime, default=datetime.utcnow)
    genre = Column(String, nullable=False)
    file_path = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)
