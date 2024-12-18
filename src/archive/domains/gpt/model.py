from gpt4all import GPT4All

from src.archive.core.base_entity import AbstractBaseEntity


class Gpt4AllModel(AbstractBaseEntity):
    def __init__(
            self, 
            model_name: str,
            references=None
    ):
        AbstractBaseEntity.__init__(self, references)
        self.model = GPT4All(model_name)

    def get_response(self, prompt: str) -> str:
        try:
            with self.model.chat_session():
                # Генерация текста потоком
                for chunk in self.model.generate(prompt, max_tokens=1024, streaming=True):
                    yield chunk  # Возвращаем каждую часть текста
        except Exception as e:
            print(f"Ошибка при генерации ответа: {e}")
            yield "Ошибка при обработке запроса."
