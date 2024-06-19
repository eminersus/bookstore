from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import database
from .. import schemas, crud


router = APIRouter()

@router.get("/genres", response_model=list[schemas.Genre])
async def get_genres(session: Session = Depends(database.get_session)) -> list[schemas.Genre]:
    return crud.get_all_genres(session)

@router.put("/genres/{genre_id}/books", response_model=schemas.Genre)
async def add_book_to_genre(genre_id: int, book_id: int, session: Session = Depends(database.get_session)) -> schemas.Genre:
    return crud.add_book_to_genre(genre_id, book_id, session)

