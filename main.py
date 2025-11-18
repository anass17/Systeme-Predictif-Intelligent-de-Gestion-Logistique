from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running!"}

@app.get("/hello")
def home():
    return {"message": "This is another page!"}
