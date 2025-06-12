from fastapi import WebSocket
from fastapi.responses import StreamingResponse

from src.archive.domains.gpt.model import Gpt4AllModel
from src.archive.service.gpt import Gpt4AllService
from src.archive.config import GPT_PATH

import os
import requests

MODEL_URL = "https://gpt4all.io/models/gguf/Meta-Llama-3-8B-Instruct.Q4_0.gguf"

def ensure_model_exists():
    if os.path.exists(GPT_PATH):
        print(f"✅ Модель уже существует по пути: {GPT_PATH}")
        return

    print(f"⬇️ Модель не найдена. Скачиваем из {MODEL_URL} ...")
    with requests.get(MODEL_URL, stream=True) as r:
        r.raise_for_status()
        os.makedirs(os.path.dirname(GPT_PATH), exist_ok=True)
        with open(GPT_PATH, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"✅ Модель успешно загружена по пути: {GPT_PATH}")

ensure_model_exists()

service = Gpt4AllService()
gpt_model = Gpt4AllModel(model_name=GPT_PATH)


def get_response_from_question(question: str):
    response_stream = service.process_text(question, gpt_model=gpt_model)
    return StreamingResponse(response_stream, media_type="text/plain")
