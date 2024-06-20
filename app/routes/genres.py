from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import database
from .. import schemas, crud
from typing import List


router = APIRouter()

@router.get("/genres", response_model=List[schemas.Genre])
async def get_genres(session: Session = Depends(database.get_session)) -> List[schemas.Genre]:
    """
    This endpoint returns all genres in the database.
    """
    return crud.get_all_genres(session)

@router.get("/genres/{genre_id}/books", response_model=List[schemas.Book])
async def get_books_by_genre_id(genre_id: int, session: Session = Depends(database.get_session)) -> List[schemas.Book]:
    """
    This endpoint returns all books in a specific genre and its subgenres.
    """
    return crud.get_books_by_genre_id(genre_id, session)

@router.post("/genres/{genre_id}/books", response_model=schemas.Genre)
async def add_book_to_genre(genre_id: int, book_id: int, session: Session = Depends(database.get_session)) -> schemas.Genre:
    """
    This endpoint adds a book to a genre. The book is specified by its ID in the request body.
    """
    return crud.add_book_to_genre(genre_id, book_id, session)

