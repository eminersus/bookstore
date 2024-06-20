from fastapi import APIRouter, Depends
from .. import schemas, crud
from ..database import database
from sqlalchemy.orm import Session
from typing import List


router = APIRouter()


@router.get("/books", response_model=list[schemas.Book])
async def get_books(db: Session = Depends(database.get_session)) -> list[schemas.Book]:
    """
    This endpoint returns all books in the database.
    """
    return crud.get_all_books(db)

@router.get("/books/{book_id}", response_model=schemas.Book)
async def get_specific_book(book_id: int, db: Session = Depends(database.get_session)) -> schemas.Book:
    """
    This endpoint returns the details of a specific book from the database.
    """
    return crud.get_book_by_id(book_id, db)

@router.post("/books", response_model=schemas.Book)
async def create_book(book_data: schemas.BookCreate, db: Session = Depends(database.get_session)) -> schemas.Book:
    """
    This endpoint creates a new book in the database.
    """
    return crud.create_book(book_data, db)

@router.delete("/books/{book_id}", response_model=schemas.Book)
async def delete_book(book_id: int, db: Session = Depends(database.get_session)) -> schemas.Book:
    """
    This endpoint deletes a book from the database.
    """
    return crud.delete_book(book_id, db)

@router.post("/books/{book_id}/authors", response_model = schemas.Book)
async def add_authors_to_book(book_id: int, request: schemas.AddAuthorsToBookRequest, db: Session = Depends(database.get_session)) -> schemas.Book:
    """
    This endpoint adds authors to a book. The authors are specified by their IDs in the request body.
    """
    return crud.add_authors_to_book(book_id, request.author_ids, db)

@router.put("/books/{book_id}", response_model = schemas.Book)
async def update_book(book_id: int, book_data: schemas.BookCreate, db: Session = Depends(database.get_session)) -> schemas.Book:
    """
    This endpoint updates a book in the database.
    """
    return crud.update_book(book_id, book_data, db)
