import sqlmodel
from .config import DATABASE_URL
from sqlmodel import SQLModel, create_engine, Session
import timescaledb

engine = timescaledb.create_engine(DATABASE_URL, timezone="UTC")

def init_db():

    SQLModel.metadata.create_all(engine)
   
    timescaledb.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session