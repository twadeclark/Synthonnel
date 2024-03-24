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
    providerurl: str
    apikey: str

@app.websocket("/ws/stream-llm-response")
async def stream_llm_response(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    itemData = json.loads(data)

    dump_text = ""
    for key, value in itemData.items():
        dump_text += f"{key}: {value}\n"

    txtTemp = dump_text + "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    lorem_ipsum = txtTemp.split()

    for word in lorem_ipsum[:len(lorem_ipsum)]:
        await asyncio.sleep(random.uniform(0.1, 0.5))
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
    if os.path.exists(json_file_path) and os.path.getsize(json_file_path) > 0:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return []

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
