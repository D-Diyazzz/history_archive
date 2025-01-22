from fastapi import WebSocket
from fastapi.responses import StreamingResponse

from src.archive.domains.gpt.model import Gpt4AllModel
from src.archive.service.gpt import Gpt4AllService
from src.archive.config import GPT_PATH


service = Gpt4AllService()
gpt_model = Gpt4AllModel(model_name=GPT_PATH)


def get_response_from_question(question: str):
    response_stream = service.process_text(question, gpt_model=gpt_model)
    return StreamingResponse(response_stream, media_type="text/plain")
