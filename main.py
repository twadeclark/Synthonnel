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

json_file_path_active = 'items-active.json'
json_file_path_saved = 'items-saved.json'

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
    item_data = json.loads(data)

    dump_text = []

    for key, value in item_data.items():
        dump_text.append(f"You sent the key {key} and the value is {value}.")

    dump_text.append("\n")
    dump_text.append("\n")

    tmplen = len(dump_text)

    dump_text.append("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
    dump_text.append("Faucibus scelerisque eleifend donec pretium.")
    dump_text.append("Eget velit aliquet sagittis id consectetur purus ut faucibus pulvinar.")
    dump_text.append("Cursus risus at ultrices mi tempus imperdiet.")
    dump_text.append("Varius vel pharetra vel turpis nunc eget lorem dolor sed.")
    dump_text.append("\n")
    dump_text.append("\n")

    dump_text = dump_text[:random.randint(tmplen, tmplen + len(dump_text) - 1)]
    random.shuffle(dump_text)
    temp_text = ' '.join(dump_text)

    await asyncio.sleep(random.uniform(0.5, 2.0))

    base_int = random.uniform(0.01, 0.3)

    for i in range(0, len(temp_text), 5):
        chunk = temp_text[i:i+5]

        await asyncio.sleep(base_int * random.uniform(0.01, 0.3))
        await websocket.send_text(chunk)

    await websocket.close()

@app.get("/get-items-active")
def get_items_active():
    with open(json_file_path_active, 'r', encoding='utf-8') as file:
        return json.load(file)

@app.post("/save-items-active")
def save_items_active(items: List[Item]):
    with open(json_file_path_active, 'w', encoding='utf-8') as file:
        items_dict = [item.dict() for item in items]
        json.dump(items_dict, file, indent=4)
    return {"message": "Items list updated successfully - active"}

@app.get("/get-items-saved")
def get_items_saved():
    with open(json_file_path_saved, 'r', encoding='utf-8') as file:
        return json.load(file)

@app.post("/save-items-saved")
def save_items_saved(items: List[Item]):
    with open(json_file_path_saved, 'w', encoding='utf-8') as file:
        items_dict = [item.dict() for item in items]
        json.dump(items_dict, file, indent=4)
    return {"message": "Items list updated successfully - saved"}

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
