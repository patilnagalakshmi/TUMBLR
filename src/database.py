'''To connect mysql to store data'''
import dataclasses
import sqlalchemy as db
from sqlalchemy import Column,String,BigInteger,JSON
from sqlalchemy.orm import declarative_base
from model import settings
Base = declarative_base()
engine = db.create_engine(settings.DATABASE_URL)
connection=engine.connect()

@dataclasses.dataclass
class ResponseRecords(Base):
    '''SQLALCHEMY ORM model '''
    __tablename__ = 'tumblr'

    id = Column(BigInteger, primary_key=True, index=True)
    status = Column(String(255), nullable=False)
    msg = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    display_text=Column(String(255),nullable=False)
    post_data=Column(JSON)
Base.metadata.create_all(engine)
