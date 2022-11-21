from typing import Union

from fastapi import FastAPI, Request

app = FastAPI()

data = {}

@app.get("/")
def read_root():
    return "hello world"

@app.post("/")
async def test(request: Request):
    body = await request.json()

    key = body.get('nim')
    value = body.get('nama')
    data[key] = value

    return data