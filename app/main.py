from fastapi import FastAPI
from .schemas import Book

app = FastAPI()

testData = {
    "books": [
        {
            "title": "The Hobbit",
            "publishedDate": "1937-09-21T00:00:00.000Z",
            "authors": ["J.R.R. Tolkien"],
            "genres": ["Fantasy"]
        },
        {
            "title": "The Fellowship of the Ring",
            "publishedDate": "1954-07-29T00:00:00.000Z",
            "authors": ["J.R.R. Tolkien"],
            "genres": ["Fantasy"]
        }
    ]
}

@app.get("/")
async def root_test():
    return {"message": "this is a root route test"}

@app.get("/books")
async def get_all_books() -> list[Book]:
    return [Book(**book) for book in testData["books"]]