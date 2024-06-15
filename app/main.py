from fastapi import FastAPI
from .schemas import Book

app = FastAPI()

testData = {
    "books": [
        {
            "title": "The Hobbit",
            "publishedDate": "1937-09-21",
            "authors": ["J.R.R. Tolkien"],
            "genres": ["Fantasy"]
        },
        {
            "title": "The Fellowship of the Ring",
            "publishedDate": "1954-07-29",
            "authors": ["J.R.R. Tolkien"],
            "genres": ["Fantasy"]
        }
    ]
}

@app.get("/")
async def root_test():
    return {"message": "this is a root route test"}

@app.get("/books")  #TODO: add query parameters here for genre, author, etc.
async def get_all_books() -> list[Book]:
    return [Book(**book) for book in testData["books"]]

@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int) -> Book:
    return Book(**testData["books"][book_id])
