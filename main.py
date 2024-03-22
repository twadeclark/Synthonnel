from typing import List
import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

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

# The path to your JSON file
json_file_path = 'items.json'


@app.post("/save-items")
def save_items(items: List[Item]):
    with open(json_file_path, 'w') as file:
        # Convert each Item instance in the list to a dict and serialize the list of dicts
        items_dict = [item.dict() for item in items]
        json.dump(items_dict, file, indent=4)
    return {"message": "Items list updated successfully"}


@app.get("/read_items")
def read_items():
    if os.path.exists(json_file_path) and os.path.getsize(json_file_path) > 0:
        with open(json_file_path, 'r') as file:
            return json.load(file)
    else:
        return []

# def write_items_to_json(items: List[dict]):
#     with open(json_file_path, 'w') as file:
#         json.dump(items, file, indent=4)

# @app.post("/add-item")
# def add_item(item: Item):
#     items = read_items_from_json()
#     items.append(item.dict())
#     write_items_to_json(items)
#     return {"message": "Item added successfully"}

# # Example endpoint to get all items
# @app.get("/items")
# def get_items():
#     return read_items_from_json()


app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
