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

def default(x, y):
    return "Not Implemented: default(x, y)" + x + y

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

