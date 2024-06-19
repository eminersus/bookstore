from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Book_DB(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    published_date = Column(String)
    authors = relationship("Author_DB", back_populates="books", secondary="book_author")
    genres = relationship("Genre_DB", back_populates="books", secondary="book_genre")

class Author_DB(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    birth_date = Column(String)
    books = relationship("Book_DB", back_populates="authors", secondary="book_author")

class Genre_DB(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    books = relationship("Book_DB", back_populates="genres", secondary="book_genre")

class book_genre_db(Base):
    __tablename__ = "book_genre"

    genre_id = Column(Integer, ForeignKey('genres.id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)

class book_author_db(Base):
    __tablename__ = "book_author"

    author_id = Column(Integer, ForeignKey('authors.id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
