import asyncio
import json
import random
import threading
from fastapi import WebSocket
from pydantic import BaseModel
from openai import OpenAI
from openai import AsyncOpenAI


class FunctionWrapper:
    def __init__(self, func, friendly_name, id):
        self.func = func
        self.friendly_name = friendly_name
        self.id = id

async def lm_studio(websocket, item_data):
    try:
        base_url = item_data["providerUrl"]
        api_key = item_data["apiKey"]

        model = item_data["model"]
        params_dict = parse_params(item_data["parameters"])

        messages = [
            {"role": "user", "content": item_data["prompt"]},
        ]

        params = {
            'messages'          : messages,
            'model'             : model,
            'stream'            : True,
            # Optional Supported OpenAI parameters:
            'timeout'           : strtofloat(params_dict.get("timeout", 60)),
            'frequency_penalty' : strtofloat(params_dict.get("frequency_penalty", None)),
            'logprobs'          : strtobool(params_dict.get("logprobs", None)),
            'max_tokens'        : strtoint(params_dict.get("max_tokens", None)),
            'n'                 : strtoint(params_dict.get("n", None)),
            'presence_penalty'  : strtofloat(params_dict.get("presence_penalty", None)),
            'seed'              : strtoint(params_dict.get("seed", None)),
            'stop'              : params_dict.get("stop", None),
            'temperature'       : strtofloat(params_dict.get("temperature", None)),
            'top_logprobs'      : strtoint(params_dict.get("top_logprobs", None)),
            'top_p'             : strtofloat(params_dict.get("top_p", None)),
            'user'              : params_dict.get("user", None)
        }

        kwargs = {k: v for k, v in params.items() if v is not None}

        client = AsyncOpenAI(base_url=base_url, api_key=api_key)




        async def main():
            stream = await client.chat.completions.create(**kwargs)
            #     model="gpt-4",
            #     messages=[{"role": "user", "content": "Say this is a test"}],
            #     stream=True,
            # )
            async for chunk in stream:
                print(chunk.choices[0].delta.content or "", end="")
                content = chunk.choices[0].delta.content
                if content:
                    await websocket.send_text(content)


        # asyncio.run(main())
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(main())
        result = await main()

        # chat_stream = client.chat.completions.create(**kwargs)

        # # pylint: disable=not-an-iterable
        # for chunk in chat_stream:
        #     content = chunk.choices[0].message.content
        #     if content:
        #         await websocket.send_text(content)

        # chat_stream.close()
        # client.close()

        return "lm_studio done."
    except Exception as e:
        print(e)
        await websocket.send_text('\n\n# Big problems. Exception: ' + str(e))
        return "lm_studio error!"


async def default(websocket: WebSocket, item_data):
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

    model_chooser = item_data["model"].lower()

    if "lightning" in model_chooser:
        for i in range(0, len(response_text), 5):
            chunk = response_text[i:i+5]
            # await asyncio.sleep(0.01) # 0.02 : 33 t/s .  0.01 : 66 t/s . 0.0 : 960 t/s . commented  : 1030 t / s
            await websocket.send_text(chunk)
    elif "fast" in model_chooser:
        for i in range(0, len(response_text), 5):
            chunk = response_text[i:i+5]
            await asyncio.sleep(0.0)
            await websocket.send_text(chunk)
    else:
        for i in range(0, len(response_text), 5):
            chunk = response_text[i:i+5]
            await asyncio.sleep(0.02)
            await websocket.send_text(chunk)

    return "default done."

async def huggingface(websocket: WebSocket, item_data):
    await asyncio.sleep(1)
    await websocket.send_text("Not Implemented: huggingface")
    return "Not Implemented: huggingface"


inference_providers = {
    "default": FunctionWrapper(default, "default", "default"),
    "LM Studio": FunctionWrapper(lm_studio, "LM Studio", "LM Studio"),
    "Hugging Face": FunctionWrapper(huggingface, "Hugging Face", "Hugging Face"),
}

class FunctionInfo(BaseModel):
    friendly_name: str
    id: str


# utility functions
def parse_params(param_string):
    params = {}
    for line in param_string.splitlines():
        if not line or line.startswith("#"):  # skip empty lines and comments
            continue
        key, value = line.strip().split("=", 1)
        params[key] = value
    return params

def strtobool(value):
    if value:
        value = value.lower()
        if value in ('y', 'yes', 't', 'true', 'on', '1'):
            return True
        elif value in ('n', 'no', 'f', 'false', 'off', '0'):
            return False
    return None

def strtoint(value):
    if value:
        try:
            return int(value)
        except ValueError:
            return None
    return None

def strtofloat(value):
    if value:
        try:
            return float(value)
        except ValueError:
            return None
    return None

