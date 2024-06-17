from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import Settings

class Database:
    def __init__(self, url: str):
        self.url = url
        self.__engine = create_engine(self.url, connect_args={"check_same_thread": False})
        self.__SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)
    def get_engine(self):
        return self.__engine

    def get_session(self):
        return self.__SessionLocal

    def init_db(self):
        from . import models
        models.Base.metadata.create_all(bind=self.__engine)


# Create a database instance
database = Database(Settings().DATABASE_URL)

    