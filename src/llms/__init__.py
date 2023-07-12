from pydantic import BaseModel
from typing import Any, List

from .chatglm import load_model as load_chatglm
from .baichuan import load_model as load_baichuan


models = {
    "THUDM/chatglm-6b": "chatglm",
    "THUDM/chatglm2-6b": "chatglm",
    "baichuan-inc/Baichuan-13B-Chat": "baichuan"
}


class LLM(BaseModel):
    id: str
    tokenizer: Any
    model: Any


def get_models():
    return list(models.keys())


llms: List[LLM] = []


def get_model(model_id: str):
    global llms

    if models.get(model_id) is None:
        raise ValueError(f"Model {model_id} not found")

    llm = next((l for l in llms if l.id == model_id), None)

    if llm is None:
        model_type = models.get(model_id)
        if model_type == "chatglm":
            model, tokenizer = load_chatglm(model_id)
        if model_type == "baichuan":
            model, tokenizer = load_baichuan(model_id)

        llm = LLM(id=model_id, tokenizer=tokenizer, model=model)
        llms.append(llm)

    return llm.model, llm.tokenizer