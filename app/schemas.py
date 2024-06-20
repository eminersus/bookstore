from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
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

class AddBookToGenreRequest(BaseModel):
    book_id: int

class AddAuthorsToBookRequest(BaseModel):
    author_ids: List[int]

class BookUpdate(BaseModel):
    # all fields are optional
    title: Optional[str] = None
    published_date: Optional[date] = None
    genres: Optional[List[int]] = None
    authors: Optional[List[int]] = None
    
Book.model_rebuild()