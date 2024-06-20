from tests.app_test import client
from app import schemas
from tests.app_test import reset_database
import pytest

@pytest.fixture(autouse=True)
def setup_and_teardown():
    reset_database()
    yield

def test_get_genres():
    response = client.get("/genres")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_books_by_genre_id():

    author_response = client.post("/authors", json={
        "full_name": "Test Author3",
        "birth_date": "2000-01-01"
    })
    author_id = author_response.json()["id"]

    book_id_1 = client.post("/books", json={
        "title": "Test Book 1",
        "published_date": "2024-01-01",
        "authors": [author_id],
        "genres": [1]
    }).json()["id"]

    book_id_2 = client.post("/books", json={
        "title": "Test Book 2",
        "published_date": "2024-01-01",
        "authors": [author_id],
        "genres": [3]
    }).json()["id"]

    book_id_3 = client.post("/books", json={
        "title": "Test Book 3",
        "published_date": "2024-01-01",
        "authors": [author_id],
        "genres": [4]
    }).json()["id"]

    book_id_4 = client.post("/books", json={
        "title": "Test Book 4",
        "published_date": "2024-01-01",
        "authors": [author_id],
        "genres": [5]
    }).json()["id"]

    book_ids_genre_1 = [book["id"] for book in client.get('/genres/1/books').json()]
    assert book_ids_genre_1 == [book_id_1, book_id_2, book_id_3, book_id_4]
    book_ids_genre_3 = [book["id"] for book in client.get('/genres/3/books').json()]
    assert book_ids_genre_3 == [book_id_2]
    book_ids_genre_4 = [book["id"] for book in client.get('/genres/4/books').json()]
    assert book_ids_genre_4 == [book_id_3, book_id_4]
    book_ids_genre_5 = [book["id"] for book in client.get('/genres/5/books').json()]
    assert book_ids_genre_5 == [book_id_4]


def test_get_books_by_genre_id_not_found():
    genre_id = 500
    response = client.get(f"/genres/{genre_id}/books")
    assert response.status_code == 404
    assert response.json() == {'detail' : f'Genre with id: {genre_id} is not found'}

def test_add_book_to_genre():
    author_response = client.post("/authors", json={
        "full_name": "Test Author2",
        "birth_date": "2000-01-01"
    })
    author_id = author_response.json()["id"]

    book = client.post('/books', json={
        "title": "Test Book 1",
        "published_date": "2024-01-01",
        "authors": [author_id],
        "genres": [1]
    }).json()
    book_id = book["id"]
    genre_id = 2
    genre_response = client.post(f"/genres/{genre_id}/books", json={
        "book_id": book_id
    })
    assert genre_response.status_code == 200
    data = genre_response.json() 
    assert data == {
        "id" : book_id,
        "published_date" : book["published_date"],
        "title" : book["title"],
        "genres": [{"name": "Fiction", "path": "/1/", "id": 1}, {"name":"Science Fiction" , "path": "/1/2/", "id": 2}],
        "authors": [{"id": author_id, "full_name": "Test Author2", "birth_date": "2000-01-01"}]
    }

