from sqlalchemy import (create_engine, Column, Integer,
                        String)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from data.config import PG_USER, PG_PASS, PG_HOST, PG_PORT, PG_DB

engine = create_engine(f'postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}')

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()



class Kitoblarim(Base):
    __tablename__ = "kitoblarim"
    id = Column(Integer, primary_key=True)
    author = Column(String(50),nullable=False)
    title = Column(String(50),nullable=False)
    keywords = Column(String(200),nullable=False)

    def save(self, session):
        session.add(self)
        session.commit()



