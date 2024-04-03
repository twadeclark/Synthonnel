from typing import List
import json
import random
from fastapi import FastAPI, WebSocket
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

    dump_text = ""
    for key, value in item_data.items():
        dump_text += f"You sent the key '{key}' and the value is '{value}'.\n"

    lorem = []

    lorem.append("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n")
    lorem.append("\nEu mi bibendum neque egestas congue. ")
    lorem.append("Faucibus et molestie ac feugiat sed lectus vestibulum mattis. ")
    lorem.append("Enim neque volutpat ac tincidunt.\n")
    lorem.append("\nConvallis aenean et tortor at risus viverra adipiscing at. ")
    lorem.append("In cursus turpis massa tincidunt dui ut ornare. ")
    lorem.append("Eu mi bibendum neque egestas congue quisque.\n")
    lorem.append("\nUrna porttitor rhoncus dolor purus. ")
    lorem.append("Vitae elementum curabitur vitae nunc sed velit dignissim sodales. ")
    lorem.append("Sed tempus urna et pharetra pharetra massa massa ultricies mi.\n")
    lorem.append("\nSagittis nisl rhoncus mattis rhoncus. ")
    lorem.append("Nibh cras pulvinar mattis nunc sed blandit libero volutpat. ")
    lorem.append("Rutrum tellus pellentesque eu tincidunt tortor aliquam nulla.\n")
    lorem.append("\nDuis tristique sollicitudin nibh sit amet commodo nulla. ")
    lorem.append("Vulputate enim nulla aliquet porttitor lacus luctus. ")
    lorem.append("Mattis pellentesque id nibh tortor id aliquet.\n")
    lorem.append("\nTurpis cursus in hac habitasse platea. ")
    lorem.append("Semper risus in hendrerit gravida rutrum quisque. ")
    lorem.append("Pulvinar neque laoreet suspendisse interdum.\n")
    lorem.append("\nIn est ante in nibh mauris. ")
    
    random.shuffle(lorem)
    
    lorem_out = lorem[:random.randint(1, len(lorem))]
    lorem_addendum = ''.join(lorem_out)
    response_text = dump_text + lorem_addendum

    for i in range(0, len(response_text), 5):
        chunk = response_text[i:i+5]
        # await asyncio.sleep(0.01) # 0.02 : 33 t/s .  0.01 : 66 t/s . 0.0 : 960 t/s . commented  : 1030 t / s
        await websocket.send_text(chunk)

    await websocket.close()


app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

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

@app.get("/get-items-templates")
def get_items_templates():
    with open(json_file_path_templates, 'r', encoding='utf-8') as file:
        return json.load(file)

@app.post("/save-items-saved")
def save_items_saved(items: List[Item]):
    with open(json_file_path_saved, 'w', encoding='utf-8') as file:
        items_dict = [item.dict() for item in items]
        json.dump(items_dict, file, indent=4)
    return {"message": "Items list updated successfully - saved"}

@app.get("/get-api-templates")
def get_functions():
    functions_info = []
    functions_info.append('')

    for func_wrapper in function_wrapper.functions.values():
        functions_info.append(function_wrapper.FunctionInfo(friendly_name=func_wrapper.friendly_name, id=func_wrapper.id))
    return functions_info

