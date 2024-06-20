from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import database
from typing import List



router = APIRouter()


@router.get("/authors", response_model=List[schemas.Author])
async def get_authors(db: Session = Depends(database.get_session)) -> List[schemas.Author]:
    """
    This endpoint returns all authors in the database.
    """
    return crud.get_all_authors(db)

@router.get("/authors/{author_id}/books", response_model=List[schemas.Book])
async def get_books_by_author_id(author_id: int, db: Session = Depends(database.get_session)) -> List[schemas.Book]:
    """
    This endpoint returns all books by a specific author.
    """
    return crud.get_books_by_author_id(author_id, db)

@router.post("/authors", response_model=schemas.Author)
async def create_author(author_data: schemas.AuthorCreate, db: Session = Depends(database.get_session)) -> schemas.Author:
    """
    This endpoint creates a new author in the database.
    """
    return crud.create_author(author_data, db)
