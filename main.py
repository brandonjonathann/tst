import json
from datetime import *
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

class User(BaseModel):
    username: str
    password: str

class Sales(BaseModel):
    item_id: int
    name: str
    category: str
    amount: int
    price: int
    date: str

class idSales(BaseModel):
    id: int

class Tanggal(BaseModel):
    interval1start: str
    interval1end: str
    interval2start: str
    interval2end: str

@app.post('/login')
def login(param: User):
    for i in range(len(akun)):
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

@app.post('/signup')
def signup(request: Request, param: User):
    authorize(request)
    found = False
    for i in range(len(akun)):
        if (param.username == akun[i]["username"]):
            found = True
    if not(found):
        password = get_hash(param.password)
        tambahan = {
            "username": param.username,
            "password": password
        }
        akun.append(tambahan)
        with open("user.json", "w") as outfile:
            outfile.write(json.dumps(akun, indent=4)) 
        return("Akun baru berhasil ditambahkan!")
    else:
        return("Username sudah digunakan")

@app.get('/tampildata')
def tampildata(request: Request):
    authorize(request)
    return sales

@app.post('/tambahdata')
def tambahdata(request: Request, param: Sales):
    authorize(request)
    jumlahdata = len(sales)
    tambahan = {
        'sales_id': jumlahdata + 1,
        'item_id': param.item_id,
        'name': param.name,
        'category': param.category,
        'amount': param.amount,
        'price': param.price,
        'date': param.date
    }
    sales.append(tambahan)
    with open("data.json", "w") as outfile:
        outfile.write(json.dumps(sales, indent=4)) 
    json.dumps(sales)
    return("Data sales berhasil ditambahkan!")

@app.post('/kurangdata')
def kurangdata(request: Request, param: idSales):
    authorize(request)
    for i in range(len(sales)):
        if (param.id == sales[i]["sales_id"]):
            sales.remove(sales[i])
            count = 1
            for i in range(len(sales)):
                sales[i]["sales_id"] = count
                count += 1
            with open("data.json", "w") as outfile:
                outfile.write(json.dumps(sales, indent=4))
            return("Data sales berhasil dihapus!")
    return("Data sales tidak ditemukan")

@app.get('/kelompokdata/item/jumlah')
def kelompokdata_jumlah_per_item(request: Request):
    authorize(request)
    item = []
    jumlah = []
    for i in range(len(sales)):
        itemada = False
        index = 0
        for j in range(len(item)):
            if (item[j] == sales[i]["name"]):
                itemada = True
                index = j
        if itemada:
            jumlah[index] += sales[i]["amount"]
        else:
            item.append(sales[i]["name"])
            jumlah.append(sales[i]["amount"])
    hasil = []
    hasil.append("category: amount")
    for i in range(len(item)):
        hasil.append(str(item[i]) + ": " + str(jumlah[i]))
    return (hasil)

@app.get('/kelompokdata/item/penjualan')
def kelompokdata_penjualan_per_item(request: Request):
    authorize(request)
    item = []
    jumlah = []
    for i in range(len(sales)):
        itemada = False
        index = 0
        for j in range(len(item)):
            if (item[j] == sales[i]["name"]):
                itemada = True
                index = j
        if itemada:
            jumlah[index] += (sales[i]["amount"] * sales[i]["price"])
        else:
            item.append(sales[i]["name"])
            jumlah.append(sales[i]["amount"] * sales[i]["price"])
    hasil = []
    hasil.append("category: amount")
    for i in range(len(item)):
        hasil.append(str(item[i]) + ": " + str(jumlah[i]))
    return (hasil)

@app.get('/kelompokdata/kategori/jumlah')
def kelompokdata_jumlah_per_kategori(request: Request):
    authorize(request)
    category = []
    jumlah = []
    for i in range(len(sales)):
        categoryada = False
        index = 0
        for j in range(len(category)):
            if (category[j] == sales[i]["category"]):
                categoryada = True
                index = j
        if categoryada:
            jumlah[index] += sales[i]["amount"]
        else:
            category.append(sales[i]["category"])
            jumlah.append(sales[i]["amount"])
    hasil = []
    hasil.append("category: amount")
    for i in range(len(category)):
        hasil.append(str(category[i]) + ": " + str(jumlah[i]))
    return (hasil)

@app.get('/kelompokdata/kategori/penjualan')
def kelompokdata_penjualan_per_kategori(request: Request):
    authorize(request)
    category = []
    jumlah = []
    for i in range(len(sales)):
        categoryada = False
        index = 0
        for j in range(len(category)):
            if (category[j] == sales[i]["category"]):
                categoryada = True
                index = j
        if categoryada:
            jumlah[index] += (sales[i]["amount"] * sales[i]["price"])
        else:
            category.append(sales[i]["category"])
            jumlah.append(sales[i]["amount"] * sales[i]["price"])
    hasil = []
    hasil.append("category: penjualan")
    for i in range(len(category)):
        hasil.append(str(category[i]) + ": " + str(jumlah[i]))
    return (hasil)

@app.get('/kelompokdata/tanggal')
def kelompokdata_tanggal(request: Request, param: Tanggal):
    authorize(request)
    interval1start = datetime.strptime(param.interval1start, '%d-%m-%Y')
    interval1end = datetime.strptime(param.interval1end, '%d-%m-%Y')
    interval2start = datetime.strptime(param.interval2start, '%d-%m-%Y')
    interval2end = datetime.strptime(param.interval2end, '%d-%m-%Y')

    jumlah = [0, 0]
    total = [0, 0]
    for i in range(len(sales)):
        temp = datetime.strptime(sales[i]["date"], '%d-%m-%Y')
        if (temp >= interval1start and temp <= interval1end):
            jumlah[0] += sales[i]["amount"]
            total[0] += (sales[i]["amount"] * sales[i]["price"])
        if (temp >= interval2start and temp <= interval2end):
            jumlah[1] += sales[i]["amount"]
            total[1] += (sales[i]["amount"] * sales[i]["price"])
    hasil = []
    hasil.append("interval: amount: penjualan")
    hasil.append(str(param.interval1start) + " to " + str(param.interval1end) + ": " + str(jumlah[0]) + ": " + str(total[0]))
    hasil.append(str(param.interval2start) + " to " + str(param.interval2end) + ": " + str(jumlah[1]) + ": " + str(total[1]))
    return (hasil)