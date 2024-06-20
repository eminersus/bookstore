from pydantic import BaseModel, Field, ConfigDict
from typing import List, Type
from datetime import date


class BookBase(BaseModel):
    title: str
    published_date: date

class BookCreate(BookBase):
    genres: List[int]
    authors: List[int]

class Book(BookBase):
    id: int
    genres: List['GenreWOBooks'] = Field(..., min_length=1)
    authors: List['AuthorWOBooks'] = Field(..., min_length=1)
    class Config:
        from_attributes=True

class AuthorBase(BaseModel):
    full_name: str
    birth_date: date

class AuthorCreate(AuthorBase):
    pass

class BookInAuthors(BookBase):
    pass

class Author(AuthorBase):
    id: int
    books: List[BookInAuthors] = []
    class Config:
        from_attributes=True

class GenreBase(BaseModel):
    name: str
    path: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int
    class Config:
        from_attributes=True

class GenreWOBooks(GenreBase):
    id: int
    class Config:
        from_attributes=True

class AuthorWOBooks(AuthorBase):
    id: int
    class Config:
        from_attributes=True

    
Book.model_rebuild()