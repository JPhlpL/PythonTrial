from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from video_fps import get_video_fps

app = FastAPI()

class Item(BaseModel):
    number1: float
    number2: float

@app.post("/add")
async def add_twonum(item: Item):
    return {"result": item.number1 + item.number2 }


@app.post("/getvideo")
async def add_twonum():
    return {"result"}

@app.get("/fps/{filepath}")
async def get_fps(filepath: str):
    fps = get_video_fps(filepath)
    return {"fps": fps}