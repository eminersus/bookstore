from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from app.main import app
from app.database.database import database
from app.models import Base
from app.database.seeder import get_seed_genre_data, insert_genre_data


SQLALCHEMY_DATABASE_URL_TEST = os.getenv("DATABASE_URL_TEST")

engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[database.get_session] = override_get_db

def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    seed_data = get_seed_genre_data()
    with TestingSessionLocal() as db:
        insert_genre_data(seed_data, db)

client = TestClient(app)

