from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import Settings
import models

class Database:
    def __init__(self, url: str):
        self.url = url
        self.__engine = create_engine(self.url)
        self.__SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_engine(self):
        return self.engine

    def get_session(self):
        return self.SessionLocal

    def init_db(self):
        models.Base.metadata.create_all(bind=self.engine)

# Create a database instance
database = Database(Settings().database_url)

    