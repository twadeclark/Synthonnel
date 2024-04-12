import asyncio
import json
import random
import httpx
from fastapi import WebSocket
from pydantic import BaseModel
from openai import AsyncOpenAI

SAVE_MOST_RECENT_RESPONSE = False

class FunctionWrapper:
    def __init__(self, func, friendly_name, id):
        self.func = func
        self.friendly_name = friendly_name
        self.id = id

async def default(websocket: WebSocket, item_data):
    await asyncio.sleep(0.5)
    await websocket.send_text("This interface is not implemented.\n")
    for key, value in item_data.items():
        await asyncio.sleep(0.5)
        await websocket.send_text(f"You sent the key '{key}' and the value is '{value}'.\n")
    return "This interface is not implemented."


async def openai(websocket, item_data):
    try:
        base_url = item_data["providerUrl"]
        api_key = item_data["apiKey"]

        model = item_data["model"]
        params_parsed = parse_params(item_data["parameters"])

        messages = item_data["messages"]

        params = {
            'messages'          : messages,
            'model'             : model,
            'stream'            : True,
            # Optional Supported OpenAI parameters:
            'timeout'           : strtofloat(params_parsed.get("timeout", 60)),
            'frequency_penalty' : strtofloat(params_parsed.get("frequency_penalty", None)),
            'logprobs'          : strtobool(params_parsed.get("logprobs", None)),
            'max_tokens'        : strtoint(params_parsed.get("max_tokens", None)),
            'n'                 : strtoint(params_parsed.get("n", None)),
            'presence_penalty'  : strtofloat(params_parsed.get("presence_penalty", None)),
            'seed'              : strtoint(params_parsed.get("seed", None)),
            'stop'              : params_parsed.get("stop", None),
            'temperature'       : strtofloat(params_parsed.get("temperature", None)),
            'top_logprobs'      : strtoint(params_parsed.get("top_logprobs", None)),
            'top_p'             : strtofloat(params_parsed.get("top_p", None)),
            'user'              : params_parsed.get("user", None)
        }

        kwargs = {k: v for k, v in params.items() if v is not None}

        client = AsyncOpenAI(base_url=base_url, api_key=api_key)

        async def streamer():

            raw_responses_most_recent_dump = ""

            try:
                stream = await client.chat.completions.create(**kwargs)
                async for chunk in stream:

                    if chunk:
                        raw_responses_most_recent_dump += str(chunk) + "\n"

                    content = chunk.choices[0].delta.content
                    if content:
                        await websocket.send_text(content)
            except Exception as e:
                print(e)
                print(e.with_traceback)
                await websocket.send_text('\n\n# THREAD Big problems. Exception: ' + str(e))
                await websocket.send_text('\n\n# THREAD Big problems. Exception with_traceback: ' + str(e.with_traceback))

            if SAVE_MOST_RECENT_RESPONSE:
                with open("scratch/raw_responses_most_recent_dump_OpenAI.txt", 'w', encoding='utf-8') as file:
                    file.write(raw_responses_most_recent_dump)

        await streamer()

        return "openai done."
    except Exception as e:
        print(e)
        await websocket.send_text('\n\n# Big problems. Exception: ' + str(e))
        return "openai error!"


async def huggingfacefree(websocket: WebSocket, item_data):
    try:
        base_url = item_data["providerUrl"]
        api_key = item_data["apiKey"]
        model = item_data["model"]
        params_parsed = parse_params(item_data["parameters"])
        messages = item_data["messages"]
        headers = {"Authorization": f"Bearer {api_key}"}
        this_api_endpoint = base_url + model

        messages_formatted_as_string = ""
        for message in messages:
            role = message['role'].upper
            content = message['content'].replace('\n',' ')
            messages_formatted_as_string += f'{role}: {content}\n'

        params = {
            "return_full_text"   : False,
            # Optional Supported Hugging Face parameters:
            'max_time'           : strtofloat(params_parsed.get("max_time", 60)),
            'do_sample'          : strtobool(params_parsed.get("do_sample", 'True')),
            'top_k'              : strtoint(params_parsed.get("top_k", None)),
            'top_p'              : strtoint(params_parsed.get("top_p", None)),
            'temperature'        : strtofloat(params_parsed.get("temperature", None)),
            'repetition_penalty' : strtofloat(params_parsed.get("repetition_penalty", None)),
            'max_new_tokens'     : strtoint(params_parsed.get("max_new_tokens", 250)),
        }

        kwargs = {k: v for k, v in params.items() if v is not None}

        payload = {
            "inputs"     : messages_formatted_as_string.strip(),
            "parameters" : kwargs,
            "options"    :    { "wait_for_model": True,
                                "use_cache": False,
                                "stream": True
                                }
            }

        async with httpx.AsyncClient() as client:
            response = await client.post(this_api_endpoint, headers=headers, json=payload, timeout=60)

        if SAVE_MOST_RECENT_RESPONSE:
            raw_responses_most_recent_dump = str(response) + "\n"
            with open("scratch/raw_responses_most_recent_dump_HuggingFaceFree.txt", 'w', encoding='utf-8') as file:
                file.write(raw_responses_most_recent_dump)

        all_chunks = response.text

        data = json.loads(all_chunks)

        target_keys = ['error', 'warning', 'warnings', 'generated_text', 'summary_text']
        results = find_keys(data, target_keys)

        content = ""

        # big problems:
        if results.get('error'):
            content += results['error']

        # small problems:
        if results.get('warning'):
            content += results['warning']

        # success stories:
        if results.get('generated_text'):
            content += results['generated_text']

        if results.get('summary_text'):
            content += results['summary_text']

        await websocket.send_text(content)

        return "huggingfacefree done."
    except Exception as e:
        print(e)
        await websocket.send_text('\n\n# Big problems. Exception: ' + str(e))
        return "huggingfacefree error!"


async def lm_studio(websocket, item_data):
    try:
        base_url = item_data["providerUrl"]
        api_key = item_data["apiKey"]

        model = item_data["model"]
        params_parsed = parse_params(item_data["parameters"])

        messages = item_data["messages"]

        params = {
            'messages'          : messages,
            'model'             : model,
            'stream'            : True,
            # Optional Supported OpenAI parameters:
            'timeout'           : strtofloat(params_parsed.get("timeout", 60)),
            'frequency_penalty' : strtofloat(params_parsed.get("frequency_penalty", None)),
            'logprobs'          : strtobool(params_parsed.get("logprobs", None)),
            'max_tokens'        : strtoint(params_parsed.get("max_tokens", None)),
            'n'                 : strtoint(params_parsed.get("n", None)),
            'presence_penalty'  : strtofloat(params_parsed.get("presence_penalty", None)),
            'seed'              : strtoint(params_parsed.get("seed", None)),
            'stop'              : params_parsed.get("stop", None),
            'temperature'       : strtofloat(params_parsed.get("temperature", None)),
            'top_logprobs'      : strtoint(params_parsed.get("top_logprobs", None)),
            'top_p'             : strtofloat(params_parsed.get("top_p", None)),
            'user'              : params_parsed.get("user", None)
        }

        kwargs = {k: v for k, v in params.items() if v is not None}

        client = AsyncOpenAI(base_url=base_url, api_key=api_key)

        async def streamer():

            raw_responses_most_recent_dump = ""

            try:
                stream = await client.chat.completions.create(**kwargs)
                async for chunk in stream:

                    if chunk:
                        raw_responses_most_recent_dump += str(chunk) + "\n"

                    content = chunk.choices[0].delta.content
                    if content:
                        await websocket.send_text(content)
            except Exception as e:
                print(e)
                print(e.with_traceback)
                await websocket.send_text('\n\n# THREAD Big problems. Exception: ' + str(e))
                await websocket.send_text('\n\n# THREAD Big problems. Exception with_traceback: ' + str(e.with_traceback))

            if SAVE_MOST_RECENT_RESPONSE:
                with open("scratch/raw_responses_most_recent_dump_LMStudio.txt", 'w', encoding='utf-8') as file:
                    file.write(raw_responses_most_recent_dump)

        await streamer()

        return "lm_studio done."
    except Exception as e:
        print(e)
        await websocket.send_text('\n\n# Big problems. Exception: ' + str(e))
        return "lm_studio error!"


async def internaltesting(websocket: WebSocket, item_data):
    dump_text = ""
    # for key, value in item_data.items():
    #     dump_text += f"You sent the key '{key}' and the value is '{value}'.\n"

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
        await asyncio.sleep(random.uniform(0.0, 1.0))
        loop_sleep = random.uniform(0.01, 0.03)
        for i in range(0, len(response_text), 5):
            chunk = response_text[i:i+5]
            await asyncio.sleep(loop_sleep)
            await websocket.send_text(chunk)

    return "Internal Testing done."


###############################
# API Template Client Code List
inference_providers = {
    "Internal Testing": FunctionWrapper(internaltesting, "Internal Testing", "Internal Testing"),
    "LM Studio": FunctionWrapper(lm_studio, "LM Studio", "LM Studio"),
    "Hugging Face Free": FunctionWrapper(huggingfacefree, "Hugging Face Free", "Hugging Face Free"),
    "OpenAI": FunctionWrapper(openai, "OpenAI", "OpenAI"),
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

def find_keys(json_input, target_keys):
    results = {}

    def _find_keys_recursive(json_fragment):
        if isinstance(json_fragment, dict):
            for key, value in json_fragment.items():
                if key in target_keys:
                    results[key] = value
                _find_keys_recursive(value)
        elif isinstance(json_fragment, list):
            for item in json_fragment:
                _find_keys_recursive(item)

    _find_keys_recursive(json_input)
    return results
