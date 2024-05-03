# Synthonnel

One Prompt, Many LLMs.

## User Guide

See the Tutorial at [Synthonnel.com](https://www.synthonnel.com/) for more information.

## Super Quick Start - From Source

#### Create and Activate Virtual Environment

```
python -m venv venv
```

- **Windows**:

```
.\venv\Scripts\activate
```

- **macOS/Linux**:

```
source venv/bin/activate
```


#### Install Required Packages:

```
pip install -r requirements.txt
```


#### Start Backend:

```
uvicorn main:app --reload
```


#### Use Browser for UI:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)


### Reference

#### Optional Supported OpenAI parameters:
    frequency_penalty: float | NotGiven | None = NOT_GIVEN,
    logprobs: bool | NotGiven | None = NOT_GIVEN,
    max_tokens: int | NotGiven | None = NOT_GIVEN,
    n: int | NotGiven | None = NOT_GIVEN,
    presence_penalty: float | NotGiven | None = NOT_GIVEN,
    seed: int | NotGiven | None = NOT_GIVEN,
    stop: str | List[str] | NotGiven | None = NOT_GIVEN,
    temperature: float | NotGiven | None = NOT_GIVEN,
    top_logprobs: int | NotGiven | None = NOT_GIVEN,
    top_p: float | NotGiven | None = NOT_GIVEN,
    user: str | NotGiven = NOT_GIVEN,
    timeout: float | Timeout | NotGiven | None = NOT_GIVEN

#### ALL OpenAI parameters:
    messages: Iterable[ChatCompletionMessageParam],
    model: str,
    frequency_penalty: float | NotGiven | None = NOT_GIVEN,
    function_call: FunctionCall | NotGiven = NOT_GIVEN,
    functions: Iterable[Function] | NotGiven = NOT_GIVEN,
    logit_bias: Dict[str, int] | NotGiven | None = NOT_GIVEN,
    logprobs: bool | NotGiven | None = NOT_GIVEN,
    max_tokens: int | NotGiven | None = NOT_GIVEN,
    n: int | NotGiven | None = NOT_GIVEN,
    presence_penalty: float | NotGiven | None = NOT_GIVEN,
    response_format: ResponseFormat | NotGiven = NOT_GIVEN,
    seed: int | NotGiven | None = NOT_GIVEN,
    stop: str | List[str] | NotGiven | None = NOT_GIVEN,
    stream: NotGiven | Literal[False] | None = NOT_GIVEN,
    temperature: float | NotGiven | None = NOT_GIVEN,
    tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
    tools: Iterable[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
    top_logprobs: int | NotGiven | None = NOT_GIVEN,
    top_p: float | NotGiven | None = NOT_GIVEN,
    user: str | NotGiven = NOT_GIVEN,
    extra_headers: Headers | None = None,
    extra_query: Query | None = None,
    extra_body: Body | None = None,
    timeout: float | Timeout | NotGiven | None = NOT_GIVEN
