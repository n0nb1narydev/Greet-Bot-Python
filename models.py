from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///members.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    techdegree = Column(String)
    verified = Column(Boolean)

    def __repr__(self):
        return f"<Member(username={self.username}, email={self.email}, techdegree={self.techdegree})>"

def initialize():
    Base.metadata.create_all(engine)