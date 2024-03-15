from src.archive.core import AbstractBaseEntity


class Type(AbstractBaseEntity):

    def __init__(
            self,
            name: str,
            id: int = None,
    ):
        self.id = id
        self.name = name

    def get_id(self):
        return self._id
    
    def get_name(self):
        return self._name