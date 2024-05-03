from typing import List
import json
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import function_wrapper

app = FastAPI()

json_file_path_active = 'items-active.json'
json_file_path_saved = 'items-saved.json'
json_file_path_templates = 'items-templates.json'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    model: str
    systemPrompt: str
    provider: str
    note: str
    providerUrl: str
    parameters: str
    apiKey: str


@app.websocket("/ws/stream-llm-response")
async def stream_llm_response(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    item_data = json.loads(data)

    provider = item_data["provider"]
    model = item_data["model"]

    if provider in function_wrapper.inference_providers:
        print(f"Inference Attempt. provider: '{provider}' model: '{model}'")
        await function_wrapper.inference_providers[provider].func(websocket, item_data)
        print(f"Inference Success. provider: '{provider}' model: '{model}'")
    else:
        print(f"Inference Failure. provider: '{provider}' not found.")

    await websocket.close()

@app.get("/get-items-active")
def get_items_active():
    try:
        with open(json_file_path_active, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save-items-active")
def save_items_active(items: List[Item]):
    with open(json_file_path_active, 'w', encoding='utf-8') as file:
        items_dict = [item.dict() for item in items]
        json.dump(items_dict, file, indent=4)
    return {"message": "Items list updated successfully - active"}

@app.get("/get-items-saved")
def get_items_saved():
    try:
        with open(json_file_path_saved, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save-items-saved")
def save_items_saved(items: List[Item]):
    with open(json_file_path_saved, 'w', encoding='utf-8') as file:
        items_dict = [item.dict() for item in items]
        json.dump(items_dict, file, indent=4)
    return {"message": "Items list updated successfully - saved"}

@app.get("/get-items-templates")
def get_items_templates():
    with open(json_file_path_templates, 'r', encoding='utf-8') as file:
        return json.load(file)

@app.get("/get-api-templates")
def get_functions():
    functions_info = []
    functions_info.append('')

    for func_wrapper in function_wrapper.inference_providers.values():
        functions_info.append(function_wrapper.FunctionInfo(friendly_name=func_wrapper.friendly_name, id=func_wrapper.id))
    return functions_info

app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
