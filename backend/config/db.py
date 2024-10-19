# backend/config/db.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import Config

Base = declarative_base()
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

def init_db(drop_and_recreate=False):
    if drop_and_recreate:
        Base.metadata.drop_all(engine)
        print("Dropped all tables in the database.")
    
    Base.metadata.create_all(engine)
    print("Initialized database with the current schema.")
