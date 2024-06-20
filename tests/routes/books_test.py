from tests.app_test import client
from tests.app_test import reset_database
import pytest

@pytest.fixture(autouse=True)
def setup_and_teardown():
    reset_database()
    yield
    
def test_create_book_author_do_not_exist():
    response = client.post("/books", json={
        "title": "Test Book",
        "published_date": "2024-01-01",
        "authors": [1],
        "genres": [1]
    })
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "One or more authors do not exist"}

def test_create_book_genre_do_not_exist():
    # first create an author
    author_response = client.post("/authors", json={
        "full_name": "Test Author",
        "birth_date": "2000-01-01"
    })
    author_id = author_response.json()["id"]

    response = client.post("/books", json={
        "title": "Test Book",
        "published_date": "2024-01-01",
        "authors": [author_id],
        "genres": [555]
    })

    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "One or more genres do not exist"}

def test_create_book():
    # first create an author
    author_response = client.post("/authors", json={
        "full_name": "Test Author",
        "birth_date": "2000-01-01"
    })
    author_id = author_response.json()["id"]

    response = client.post("/books", json={
        "title": "Test Book",
        "published_date": "2024-01-01",
        "authors": [author_id],
        "genres": [1]
    })

    assert response.status_code == 200, response.text
    assert response.json() == {
        "id": 1,
        "title": "Test Book",
        "published_date": "2024-01-01",
        "genres": [
            {
                "id": 1,
                "name": "Fiction",
                "path": "/1/"
            }
        ],
        "authors": [
            {
                "id": author_id,
                "full_name": "Test Author",
                "birth_date": "2000-01-01"
            }
        ]
    }


def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_specific_book():
    author_response = client.post("/authors", json={
        "full_name": "Test Author",
        "birth_date": "2000-01-01"
    })
    author_id = author_response.json()["id"]

    response = client.post("/books", json={
        "title": "Test Book",
        "published_date": "2024-01-01",
        "authors": [author_id],
        "genres": [1]
    })
    book_id = response.json()["id"]
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["published_date"] == "2024-01-01"

def test_get_specific_book_not_found():
    book_id = 1
    response = client.get(f'/books/{book_id}')
    assert response.status_code == 404
    assert response.json() == {'detail': f'Book with id: {book_id} is not found'}

def test_delete_book():
    author_response = client.post("/authors", json={
        "full_name": "Test Author",
        "birth_date": "2000-01-01"
    })
    response = client.post("/books", json={
        "title": "Test Book",
        "published_date": "2024-01-01",
        "authors": [1],
        "genres": [1]
    })
    book_id = response.json()["id"]
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book_id

def test_update_book():
    client.post("/authors", json={
        "full_name": "Test Author",
        "birth_date": "2000-01-01"
    })
    client.post("/authors", json={
        "full_name": "Test Author 2",
        "birth_date": "2000-01-01"
    })
    response = client.post("/books", json={
        "title": "Test Book",
        "published_date": "2024-01-01",
        "authors": [1],
        "genres": [1]
    })
    book_id = response.json()["id"]
    response = client.put(f"/books/{book_id}", json={
        "title": "Updated Test Book",
        "published_date": "2025-01-01",
        "authors": [2],
        "genres": [2]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Test Book"
    assert data["published_date"] == "2025-01-01"
    assert data["authors"][0]["id"] == 2
    assert data["genres"][0]["id"] == 2

def test_update_book_not_found():
    book_id = 1
    response = client.put(f"/books/{book_id}", json={
        "title": "Updated Test Book",
        "published_date": "2025-01-01",
        "authors": [2],
        "genres": [2]
    })
    assert response.status_code == 404
    assert response.json() == {'detail': f'Book with id: {book_id} is not found'}

def test_add_authors_to_book():
    author_response = client.post("/authors", json={
        "full_name": "Test Author1",
        "birth_date": "2000-01-01"
    })
    author_id_1 = author_response.json()["id"]

    author_response_2 = client.post("/authors", json={
        "full_name": "Test Author2",
        "birth_date": "2000-01-01"
    })
    author_id_2 = author_response_2.json()["id"]

    author_response_3 = client.post("/authors", json={
        "full_name": "Test Author3",
        "birth_date": "2000-01-01"
    })
    author_id_3 = author_response_3.json()["id"]

    book = client.post("/books", json={
        "title": "Test Book",
        "published_date": "2024-01-01",
        "authors": [author_id_1],
        "genres": [1]
    }).json()
    book_id = book["id"]
    author_response = client.post(f"/books/{book_id}/authors", json={
        "author_ids": [author_id_2, author_id_3]
    })

    assert author_response.status_code == 200
    data = author_response.json()
    expected_response = {
        "id": book_id,
        "published_date" : book["published_date"],
        "title" : book["title"],
        "genres": [{"name": "Fiction", "path": "/1/", "id": 1}],
        "authors": [{"id": author_id_1, "full_name": "Test Author1", "birth_date": "2000-01-01"}, 
                    {"id": author_id_2, "full_name": "Test Author2", "birth_date": "2000-01-01"},
                    {"id": author_id_3, "full_name": "Test Author3", "birth_date": "2000-01-01"}]
    }
    data["authors"] = sorted(data["authors"], key=lambda x: x["id"])
    expected_response["authors"] = sorted(expected_response["authors"], key=lambda x: x["id"])

    assert data == expected_response
