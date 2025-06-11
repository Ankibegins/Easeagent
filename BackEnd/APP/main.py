from fastapi import FastAPI
from APP.routes import user

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "easeagent backend is working woooooooo!"}
