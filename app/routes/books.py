from fastapi import APIRouter, Depends
from .. import schemas, crud
from ..database import database
from sqlalchemy.orm import Session
from typing import List


router = APIRouter()


@router.get("/books", response_model=list[schemas.Book])
async def get_books(author_id: int | None = None , genre_id: int | None = None, db: Session = Depends(database.get_session)) -> list[schemas.Book]:
    if author_id is not None and genre_id is not None:
        return []
    
    elif author_id is not None:
        return crud.get_books_by_author_id(author_id, db)
    
    elif genre_id is not None:
        return crud.get_books_by_genre_id(genre_id, db)
    
    else:
        return crud.get_all_books(db)

@router.get("/books/{book_id}", response_model=schemas.Book)
async def get_specific_book(book_id: int, db: Session = Depends(database.get_session)) -> schemas.Book:
    return crud.get_book_by_id(book_id, db)

@router.post("/books", response_model=schemas.Book)
async def create_book(book_data: schemas.BookCreate, db: Session = Depends(database.get_session)) -> schemas.Book:
    return crud.create_book(book_data, db)

@router.delete("/books/{book_id}", response_model=schemas.Book)
async def delete_book(book_id: int, db: Session = Depends(database.get_session)) -> schemas.Book:
    return crud.delete_book(book_id, db)

@router.put("/books/{book_id}/authors", response_model = schemas.Book)
async def add_authors_to_book(book_id: int, author_ids: List[int], db: Session = Depends(database.get_session)) -> schemas.Book:
    return crud.add_authors_to_book(book_id, author_ids, db)

@router.put("/books/{book_id}", response_model = schemas.Book)
async def update_book(book_id: int, book_data: schemas.BookCreate, db: Session = Depends(database.get_session)) -> schemas.Book:
    return crud.update_book(book_id, book_data, db)
