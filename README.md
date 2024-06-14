# Bookstore API
This project is built using FastAPI and SQLite. A simple API for a bookstore enabling users to add, update, delete and view books based on their title, author, and genre.

## Installation

1. Clone the repository
```bash
git clone https://github.com/eminersus/bookstore.git
```
2. Change the directory
```bash
cd bookstore
```
3. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate
```
4. Install the dependencies from the requirements.txt file
```bash
pip install -r requirements.txt
```
5. Run the application for local deployment only
```bash
uvicorn app.main:app --reload --host
```