from src.archive.domains.gpt import Gpt4AllModel


class Gpt4AllService:

    def process_text(self, question: str, gpt_model: Gpt4AllModel) -> str:
        return gpt_model.get_response(question)
