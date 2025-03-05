from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from datetime import datetime
import os

app = FastAPI()

# Configure Jinja2Templates
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/newHTML")
async def read_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
