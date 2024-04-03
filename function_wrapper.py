import json
import random
from fastapi import WebSocket
from pydantic import BaseModel


class FunctionWrapper:
    def __init__(self, func, friendly_name, id):
        self.func = func
        self.friendly_name = friendly_name
        self.id = id

def add(x, y):
    return "Not Implemented: add(x, y)" + x + y

def subtract(x, y):
    return "Not Implemented: subtract(x, y)" + x + y

async def default(websocket: WebSocket):
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

    return "default must have worked."

def lm_studio(x, y):
    return "Not Implemented: lm_studio(x, y)" + x + y

def huggingface(x, y):
    return "Not Implemented: huggingface(x, y)" + x + y

functions = {
    "ADD": FunctionWrapper(add, "Add", "ADD"),
    "SUB": FunctionWrapper(subtract, "Subtract", "SUB"),
    "default": FunctionWrapper(default, "default", "default"),
    "LM Studio": FunctionWrapper(lm_studio, "LM Studio", "LM Studio"),
    "Hugging Face": FunctionWrapper(huggingface, "Hugging Face", "Hugging Face"),
}

class FunctionInfo(BaseModel):
    friendly_name: str
    id: str
