import threading
from fastapi import FastAPI

app = FastAPI()
set_free()

@app.get("/")
def read_root():
    return {"Hello": "World"}
