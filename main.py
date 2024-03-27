from typing import List
import json
import os
import asyncio
import random
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

json_file_path = 'items.json'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    provider: str
    model: str
    parameters: str
    providerUrl: str
    apiKey: str

@app.websocket("/ws/stream-llm-response")
async def stream_llm_response(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    itemData = json.loads(data)

    dump_text = ""
    for key, value in itemData.items():
        dump_text += f"{key}: {value}\n"

    # lorem = " Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Faucibus scelerisque eleifend donec pretium. Eget velit aliquet sagittis id consectetur purus ut faucibus pulvinar. Cursus risus at ultrices mi tempus imperdiet. Varius vel pharetra vel turpis nunc eget lorem dolor sed. Quam adipiscing vitae proin sagittis nisl. Enim blandit volutpat maecenas volutpat blandit aliquam etiam. Vivamus arcu felis bibendum ut tristique et egestas quis. Amet volutpat consequat mauris nunc. Ut pharetra sit amet aliquam id diam maecenas ultricies. Nisl vel pretium lectus quam id leo in vitae. At ultrices mi tempus imperdiet."
    lorem = " Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Faucibus scelerisque eleifend donec pretium. Eget velit aliquet sagittis id consectetur purus ut faucibus pulvinar. Cursus risus at ultrices mi tempus imperdiet. Varius vel pharetra vel turpis nunc eget lorem dolor sed."
    temp_text = dump_text + lorem
    split_text = temp_text.split()
    split_trunc = split_text[:random.randint( len(dump_text.split()), len(split_text) - 1)]

    base_int = random.uniform(0.01, 0.1)
    await asyncio.sleep(base_int + random.uniform(0.5, 2.0))

    for word in split_trunc[:len(split_trunc) - 1]:
        await asyncio.sleep(base_int + random.uniform(0.01, 0.1))
        await websocket.send_text(word)

    await websocket.close()

@app.post("/save-items")
def save_items(items: List[Item]):
    with open(json_file_path, 'w', encoding='utf-8') as file:
        items_dict = [item.dict() for item in items]
        json.dump(items_dict, file, indent=4)
    return {"message": "Items list updated successfully"}

@app.get("/get-items")
def get_items():
    with open(json_file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
