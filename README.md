# Bookstore API
This project is built using FastAPI and SQLite. A simple API for a bookstore enabling users to add, update, delete and view books based on their title, author, and genre.

## Installation

1. Clone the repository
```bash
git clone https://github.com/eminersus/bookstore.git
```
2. Change the directory to the root of the project
```bash
cd bookstore
```
3. Set the environment variables in the .env file such as the sqlite database url
```bash
DATABASE_URL=sqlite:///example.db
```
4. Run the script under the scripts directory to create a python virtual environment, install the dependencies, and set the environment variables from the .env file
```bash
source ./scripts/setup.sh
```
(You may need to give the script execution permission to run it)
```bash
chmod +x ./scripts/setup.sh
```
5. Run the application for local deployment only
```bash
uvicorn app.main:app --reload
```