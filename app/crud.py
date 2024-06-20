from sqlalchemy.orm import Session

from fastapi import HTTPException
from . import models
from . import schemas


def get_all_genres(db: Session):
    return db.query(models.Genre_DB).all()

def get_all_books(db: Session):
    return db.query(models.Book_DB).all()

def get_books_by_genre_id(genre_id: int, db: Session):
    genre = db.query(models.Genre_DB).filter(models.Genre_DB.id == genre_id).first()
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    genre_path = genre.path
    subgenres = db.query(models.Genre_DB).filter(models.Genre_DB.path.like(f"{genre_path}%")).all()
    genre_ids = [genre.id for genre in subgenres]
    return db.query(models.Book_DB).join(models.book_genre_db).filter(models.book_genre_db.genre_id.in_(genre_ids)).distinct(models.Book_DB.id).all()

def get_books_by_author_id(author_id: int, db: Session):
    return db.query(models.Book_DB).join(models.book_author_db).filter(models.book_author_db.author_id == author_id).all()

def get_book_by_id(book_id: int, db: Session):
    book = db.query(models.Book_DB).filter(models.Book_DB.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

def create_genre(genre: schemas.GenreCreate, db: Session):
    db_genre = models.Genre_DB(name=genre.name, path=genre.path)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre.id

def get_all_authors(db: Session):
    return db.query(models.Author_DB).all()

def create_book(book_data: schemas.BookCreate, db: Session) -> schemas.Book:
    new_book = models.Book_DB(title=book_data.title, published_date=book_data.published_date)

    authors = db.query(models.Author_DB).filter(models.Author_DB.id.in_(book_data.authors)).all()
    if len(authors) != len(book_data.authors):
        raise HTTPException(status_code=400, detail="One or more authors do not exist")
    
    genres = db.query(models.Genre_DB).filter(models.Genre_DB.id.in_(book_data.genres)).all()
    if len(genres) != len(book_data.genres):
        raise HTTPException(status_code=400, detail="One or more genres do not exist")
    
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    for author in authors:
        db.add(models.book_author_db(book_id=new_book.id, author_id=author.id))
    for genre in genres:
        db.add(models.book_genre_db(book_id=new_book.id, genre_id=genre.id))
    
    db.commit()
    db.refresh(new_book)

    return new_book

def create_author(author_data: schemas.Author, db: Session) -> schemas.Author:
    new_author = models.Author_DB(full_name=author_data.full_name, birth_date=author_data.birth_date)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author

def delete_book(book_id: int, db: Session) -> schemas.Book:
    book = db.query(models.Book_DB).filter(models.Book_DB.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    return book

def add_authors_to_book(book_id: int, author_ids: list[int], db: Session) -> schemas.Book:
    book = db.query(models.Book_DB).filter(models.Book_DB.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    authors = db.query(models.Author_DB).filter(models.Author_DB.id.in_(author_ids)).all()
    if len(authors) != len(author_ids):
        raise HTTPException(status_code=400, detail="One or more authors do not exist")
    for author in authors:
        if author not in book.authors:
            book.authors.append(author)
    db.commit()
    db.refresh(book)
    return book

def add_book_to_genre(genre_id: int, book_id: int, db: Session) -> schemas.Book:
    genre = db.query(models.Genre_DB).filter(models.Genre_DB.id == genre_id).first()
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    book = db.query(models.Book_DB).filter(models.Book_DB.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if book not in genre.books:
        genre.books.append(book)
    db.commit()
    db.refresh(book)
    return book

def update_book(book_id: int, book_data: schemas.BookUpdate, db: Session) -> schemas.Book:
    book = db.query(models.Book_DB).filter(models.Book_DB.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book_data.title:
        book.title = book_data.title

    if book_data.published_date:
        book.published_date = book_data.published_date

    if book_data.authors:
        authors = db.query(models.Author_DB).filter(models.Author_DB.id.in_(book_data.authors)).all()
        if len(authors) != len(book_data.authors):
            raise HTTPException(status_code=400, detail="One or more authors do not exist")
        book.authors = authors
        
    if book_data.genres:
        genres = db.query(models.Genre_DB).filter(models.Genre_DB.id.in_(book_data.genres)).all()
        if len(genres) != len(book_data.genres):
            raise HTTPException(status_code=400, detail="One or more genres do not exist")
        book.genres = genres
    
    db.commit()
    db.refresh(book)
    return book
