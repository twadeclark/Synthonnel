from typing import List
import json
import os
import asyncio
import random
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# import httpx
from pydantic import BaseModel

app = FastAPI()

# The path to your JSON file
json_file_path = 'items.json'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify domains as needed, use ["*"] for development only
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
    lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.".split()
    for word in lorem_ipsum[:20]:
        await asyncio.sleep(random.uniform(0.1, 0.5))  # Random delay between 100ms and 500ms
        await websocket.send_text(word)
    await websocket.close()

# @app.websocket("/ws/stream-responses")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     async with httpx.AsyncClient() as client:
#         async with client.stream("POST", "LLM_PROVIDER_STREAM_URL", data={"prompt": "Your prompt here"}) as response:
#             async for line in response.aiter_lines():
#                 # Stream the line to the frontend
#                 await websocket.send_text(line)
#     await websocket.close()

@app.post("/save-items")
def save_items(items: List[Item]):
    with open(json_file_path, 'w', encoding='utf-8') as file:
        # Convert each Item instance in the list to a dict and serialize the list of dicts
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
