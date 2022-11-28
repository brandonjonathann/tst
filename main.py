import json
from typing import Union
from fastapi import FastAPI, Response, status, Header, Request, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel
from utils import get_hash, encode_token, SECRET, authorize
import jwt
load_dotenv()

app = FastAPI()

# data = {}

# @app.get("/")
# def read_root():
#     return "hello world"

# @app.post("/")
# async def test(request: Request):
#     body = await request.json()

#     key = body.get('nim')
#     value = body.get('nama')
#     data[key] = value

#     return data

with open("user.json", "r") as read_file:
    akun = json.load(read_file)

with open("data.json", "r") as read_file:
    sales = json.load(read_file)

class LoginParamater(BaseModel):
    username: str
    password: str

class Sales(BaseModel):
    nama_toko: str
    nama_barang: str
    jumlah_terjual: int
    harga: int
    tanggal_penjualan: str

@app.post('/login')
def login(param: LoginParamater):
    for i in range(len(akun)) :
        if (param.username == akun[i]["username"]):
            if (get_hash(param.password) == akun[i]["password"]):
                token = encode_token(param.username)
                return { 
                    "message": "Login Sukses",
                    "data": { "token": token }
                }
            else:
                raise HTTPException(400, "Username or password invalid")
    raise HTTPException(400, "Username or password invalid")

@app.get('/sales')
def get_sales(request: Request):
    authorize(request)
    return sales
