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
        print(prompt)
        return self.model.generate(prompt)
