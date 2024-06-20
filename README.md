# **Bookstore API**

This project is built using **FastAPI** and **SQLite**. It is a simple API for a bookstore, enabling users to add, update, delete, and view books based on their title, author, and genre.

## **Requirements**
- **Python 3.11** or higher
- **Terminal**

## **Features**
This API provides the following features:
- Add a new book
- Add a new author
- Add author(s) to an existing book
- Add a book to a genre
- Delete a specific book
- Update details of a specific book
- Show details of a specific book with author and genre information
- List all genres
- List all books
- List all authors
- List all books of an author
- List all books in a specific genre (and its subgenres!)

## **Installation**

1. **Clone the repository:**
    ```bash
    git clone https://github.com/eminersus/bookstore.git
    ```

2. **Change the directory to the root of the project:**
    ```bash
    cd bookstore
    ```

3. **Set the environment variables in the `.env` file:**
    ```plaintext
    DATABASE_URL=sqlite:///example.db 
    DATABASE_URL_TEST=sqlite:///test.db
    ```

4. **Run the setup script to create a virtual environment, install dependencies, and set environment variables:**
    ```bash
    source ./scripts/setup.sh
    ```
    (You may need to give the script execution permission to run it)
    ```bash
    chmod +x ./scripts/setup.sh
    ```

5. **Run the application for local deployment:**
    ```bash
    uvicorn app.main:app --reload
    ```

## **Usage**
By default, the application will start on `http://127.0.0.1:8000`. You can access the **Swagger UI** by visiting `http://127.0.0.1:8000/docs`. You can test the API endpoints using the Swagger UI or an API testing tool like **Postman**. 

## **Pydantic Schemas**
The Pydantic schemas are used to validate the request and response data. The schemas are defined in the `schemas.py` file and can be seen in the **Swagger UI**. The schemas are used to validate the request data in the API endpoints and to return the response data. Some of the main schemas are listed below:

| **Schema**                 |
|----------------------------|
| BookCreate                 |
| BookUpdate                 |
| Book                       |
| AuthorCreate               |
| Author                     |
| Genre                      |
| AddBookToGenreRequest      |
| AddAuthorsToBookRequest    |

Required and optional fields can be seen in **Swagger UI** for each schema.

## **Database**
The SQLite database is used to store the data. The database is created using **SQLAlchemy ORM**. The database models are defined in the `models.py` file. The database models are used to create the tables in the database and to perform CRUD operations on the tables. There are three main tables in the database:

| **Table** | **Fields**                       |
|-----------|----------------------------------|
| Books     | id, title, publication_date      |
| Authors   | id, full_name, birth_date        |
| Genres    | id, name, path                   |

There is a many-to-many relationship between the Books and Authors tables. The relationship is defined using the association table `book_authors`. Also, there is a many-to-many relationship between the Books and Genres tables. The relationship is defined using the association table `book_genres`.

### **Genre Tree in the Database**
Genres are initially given as a hierarchical data structure as can be seen under `app/resources/genre_tree.json`. The data is loaded into the database, and the genre tree is created using the `path` field in the Genres table. Every genre has a `path` field that contains the path of the genre in the genre tree. This `path` field is used to find all the subgenres of a genre with a simple query rather than using recursive queries. An example path is shown below:
```plaintext
1. Fiction
    2. Mystery
        3. Crime
    4. Romance
```
The `path` field of the Crime genre will be `/1/2/3/`. The `path` field of the Romance genre will be `/1/4/`.

## **Testing**
The tests of the endpoints are written using **Pytest**. The root folder of the tests is the `tests/` directory. To run the tests, you can use the following command directly in the terminal while on the root directory of the project:
```bash
pytest
```
**Pytest** automatically discovers the tests in the `tests/` directory and runs them. The test database is isolated from the main database, and the data is not shared between the tests. The test database is created using the `DATABASE_TEST_URL` environment variable in the `.env` file.

## **Summary**
This API is a simple bookstore API that provides basic CRUD operations for books, authors, and genres. To contact, you can reach me at [eminersus@gmail.com](mailto:eminersus@gmail.com).