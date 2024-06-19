from fastapi import FastAPI
from .database import database
from .routes import authors, genres, books


app = FastAPI(lifespan=database.init_db)

app.include_router(authors.router)
app.include_router(genres.router)
app.include_router(books.router)

