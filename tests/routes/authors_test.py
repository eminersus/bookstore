from tests.app_test import client
from tests.app_test import reset_database
import pytest

@pytest.fixture(autouse=True)
def setup_and_teardown():
    reset_database()
    yield

def test_create_author():
    response = client.post("/authors", json={
        "full_name": "Test Author1",
        "birth_date": "2000-01-01"
    })

    assert response.status_code == 200, response.text
    assert response.json() == {
        "id": 1,
        "full_name": "Test Author1",
        "birth_date": "2000-01-01",
        "books": []
    }

def test_get_books_by_author_id():
    author_response = client.post("/authors", json={
        "full_name": "Test Author2",
        "birth_date": "2000-01-01"
    })
    author_id = author_response.json()["id"]

    response = client.get(f"/authors/{author_id}/books")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_books_by_author_id_author_not_found(): #TODO first implement author_id check 
    author_id = 1
    response = client.get(f'/authors/{author_id}/books')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_authors():
    response = client.get("/authors")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)