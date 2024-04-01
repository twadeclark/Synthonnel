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
    item_data = json.loads(data)

    dump_text = []
    dump_text.append("That is an excellent question. I'm glad you asked. Here is the information you requested.")
    dump_text.append("Do you know my good friends lorem and ipsum? Here is their story.")
    dump_text.append("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Faucibus scelerisque eleifend donec pretium. Eget velit aliquet sagittis id consectetur purus ut faucibus pulvinar. Cursus risus at ultrices mi tempus imperdiet. Varius vel pharetra vel turpis nunc eget lorem dolor sed.")

    for key, value in item_data.items():
        dump_text.append(f"You sent the key {key} and the value is {value}.")

    await asyncio.sleep(random.uniform(0.5, 2.0))

    base_int = random.uniform(0.01, 0.3)
    random.shuffle(dump_text)
    dump_text = dump_text[random.randint(1, 4):]
    temp_text = '\n\n'.join(dump_text)

    for i in range(0, len(temp_text), 5):
        chunk = temp_text[i:i+5]

        await asyncio.sleep(base_int * random.uniform(0.01, 0.3))
        await websocket.send_text(chunk)

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
