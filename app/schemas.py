from pydantic import BaseModel, Field, conlist
from typing import List
from datetime import datetime, date

class Book(BaseModel):
    title: str
    published_date: date = Field(..., alias="publishedDate")
    authors: List[str] = Field(..., min_length=1) # TODO: change these to @validate
    genres: List[str] = Field(..., min_length=1) # TODO: change these to @validate

class Author(BaseModel):
    full_name: str = Field(..., alias="fullName")
    birth_date: date = Field(..., alias="birthDate")
    books: List[Book] = []

class GenreBase(BaseModel):
    name: str
    path: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int
