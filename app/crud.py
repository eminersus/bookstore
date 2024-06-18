from sqlalchemy.orm import Session
from . import models
from . import schemas


def create_genre(session: Session, genre: schemas.GenreCreate):
    db_genre = models.Genre(name=genre.name, parent_id=genre.parent_id)
    session.add(db_genre)
    session.commit()
    session.refresh(db_genre)
    return db_genre.id
