from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root_test():
    return {"message": "this is a root route test"}

