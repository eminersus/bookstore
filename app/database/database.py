from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import Settings
from .. import models
from .seeder import get_seed_genre_data, insert_genre_data
from contextlib import asynccontextmanager
from fastapi import FastAPI

class Database:
    def __init__(self, url: str):
        self.url = url
        self.__engine = create_engine(self.url, connect_args={"check_same_thread": False})
        self.__SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)
    
    def get_session(self):
        db = self.__SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def init_db_tables(self):
        models.Base.metadata.create_all(bind=self.__engine)

    def insert_seed_genres_data(self):
        data = get_seed_genre_data()
        db = self.__SessionLocal()
        insert_genre_data(data, db)
        db.close()

    @asynccontextmanager
    async def init_db(self, app: FastAPI):
        self.init_db_tables()
        self.insert_seed_genres_data()
        yield
        self.__engine.dispose()


# Create a database instance
database = Database(Settings().DATABASE_URL)

