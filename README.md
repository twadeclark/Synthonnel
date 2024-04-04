# Synthonnel

Directions

# Basics:

Create the vitual environment:

python -m venv venv


Start the vitual environment:

.\venv\Scripts\activate


Freeze your pip:

Pip Freeze:

pip freeze > requirements.txt


# To run from source:


Start FastAPI backend:

uvicorn main:app --reload


Start webserver for front end:

cd .\frontend\

python -m http.server 8080


Go here for UI:

http://localhost:8080/


# Optional Supported OpenAI parameters:
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


# ALL OpenAI parameters:
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

