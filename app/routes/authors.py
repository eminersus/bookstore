from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import database



router = APIRouter()


@router.get("/authors", response_model=list[schemas.Author])
async def get_authors(db: Session = Depends(database.get_session)) -> list[schemas.Author]:
    return crud.get_all_authors(db)

@router.post("/authors", response_model=schemas.Author)
async def create_author(author_data: schemas.AuthorCreate, db: Session = Depends(database.get_session)) -> schemas.Author:
    return crud.create_author(author_data, db)
