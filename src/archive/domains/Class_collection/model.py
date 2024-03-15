from src.archive.core import AbstractBaseEntity


class ClassCollection(AbstractBaseEntity):

    def __init__(
            self,
            name: str,
            id: int = None,
    ):
        self._id = id
        self._name = name

    def get_id(self):
        return self._id
    
    def get_name(self):
        return self._name