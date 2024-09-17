from abc import ABC, abstractmethod
from src.archive.core import AbstractBaseEntity


class AbstractRepository(ABC):

    @abstractmethod
    async def add(self, model: AbstractBaseEntity):
        raise NotImplementedError
    
    @abstractmethod
    async def get(self, id) -> AbstractBaseEntity:
        raise NotImplementedError
    
    @abstractmethod
    async def get_list(self) -> list[AbstractBaseEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, model: AbstractBaseEntity):
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, id):
        raise NotImplementedError


class AbstractLinkRepository(ABC):

    @abstractmethod
    async def add(self, obj_id, related_obj_id, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, obj_id, related_obj_id, **kwargs):
        raise NotImplementedError
