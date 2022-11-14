from bin.consumer import *
from bin.helper import *
import threading
from fastapi import FastAPI



app = FastAPI()
set_free()

c = threading.Thread(target=consume)
c.start()

@app.get("/")
def read_root():
    return {"Hello": "World"}
