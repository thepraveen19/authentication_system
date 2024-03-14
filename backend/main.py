# backend/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/data")
def get_data():
    # Example: Return dummy data
    return {"message": "Data from FastAPI Backend", "value": 42}
 