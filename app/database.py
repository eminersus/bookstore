from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import Settings
from . import models
from .seeder import get_seed_genre_data, insert_genre_data
from contextlib import contextmanager

class Database:
    def __init__(self, url: str):
        self.url = url
        self.__engine = create_engine(self.url, connect_args={"check_same_thread": False})
        self.__SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)
    def get_engine(self):
        return self.__engine

    def __get_session_local(self):
        return self.__SessionLocal
    
    @contextmanager
    def get_session(self):
        db = self.__get_session_local()
        try:
            yield db()
        finally:
            db().close()

    def init_db(self):
        models.Base.metadata.create_all(bind=self.__engine)

    def insert_seed_genres_data(self):
        with self.get_session() as session:
            data = get_seed_genre_data()
            insert_genre_data(data, session)


# Create a database instance
database = Database(Settings().DATABASE_URL)

