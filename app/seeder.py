from json import load
from . import crud
from . import schemas
from sqlalchemy.orm import Session


def get_seed_genre_data():
    with open("./app/data/genre_tree.json") as file:
        genres = load(file)
        return genres
    
def insert_genre_data(data, session: Session, parent_path="/"):
    for item in data:
        genre = schemas.GenreCreate(name=item["name"], path=f"{parent_path}{item["id"]}/")
        crud.create_genre(genre, session)
        if "children" in item:
            insert_genre_data(item["children"], session, genre.path)