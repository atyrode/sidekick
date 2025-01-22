from ollama import Client
from ollama._types import ChatResponse, ListResponse

from config import MODEL, ollama


def pull_model(ollama: Client, model: str) -> None:
    model_pulled: bool = _is_model_pulled(ollama, model)
    if not model_pulled:
        ollama.pull(model)

def _is_model_pulled(ollama: Client, model: str) -> bool:
    response: ListResponse = ollama.list()
    return model in response.models

def chat(ollama: Client, model: str, messages: list[dict]) -> ChatResponse: 
    response: ChatResponse = ollama.chat(model, messages)
    return response