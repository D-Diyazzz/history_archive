from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from src.archive.core import AbstractBaseEntity, AbstractRepository, AbstractLinkRepository, repository
from src.archive.repository.repository_factory import RepositoryFactory


class AbstractUnitOfWork(ABC):
    repository: AbstractRepository
    link_repository: AbstractLinkRepository

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError
    
    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class AbstractUnitOfWork2(ABC):

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError
    
    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

    @abstractmethod
    async def get_repository(self, obj_type):
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: AbstractBaseEntity):
        raise NotImplementedError

    @abstractmethod
    async def add_link(self, obj_id, related_obj_id, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id, obj_type):
        raise NotImplementedError

    @abstractmethod
    async def get(self, id, obj_type):
        raise NotImplementedError

    @abstractmethod
    async def update(eslf, model: AbstractBaseEntity):
        raise NotImplementedError
    

class UnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory: AsyncSession, reposiotry: AbstractRepository=None, link_repository: AbstractLinkRepository=None):
        self.session_factory = session_factory
        self.repository = reposiotry
        self.link_repository = link_repository

    async def __aenter__(self):
        self.session = await self.session_factory()
        self.repository = self.repository(self.session) if self.repository else None
        self.link_repository = self.link_repository(self.session) if self.link_repository else None
        return await super().__aenter__()
    
    async def __aexit__(self, *args):
        await super().__aexit__()
        await self.session.close()
        self.repository = self.repository.__class__ if self.repository else None
        self.link_repository = self.link_repository.__class__ if self.link_repository else None

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

class UnitOfWork2(AbstractUnitOfWork2):
    
    def __init__(self, session_factory: AsyncSession, repository_factory: RepositoryFactory):
        self.session_factory = session_factory
        self.repositories = {}
        self.repository_factory = repository_factory

    async def __aenter__(self):
        self.session = await self.session_factory()
        self.repository_factory = self.repository_factory(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__()
        await self.session.close()
        self.repositories = {}
        self.repository_factory = self.repository_factory.__class__

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def add(self, model: AbstractBaseEntity):
        repository = await self.get_repository(type(model))
        response = await repository.add(model)
        return response

    async def add_link(self, obj_type, obj_id, related_obj_id, **kwargs):
        repository = await self.get_repository(obj_type)
        response = await reposiotry.add(obj_id, related_obj_id, kwargs)
        return response
    
    async def get_repository(self, obj_type):
        repo = self.repositories.get(obj_type)
        if repo is None:
            repo = self.repository_factory.get_repository(obj_type)
            print(obj_type)
            self.repositories[obj_type] = repo
        return repo

    async def delete(self, id, obj_type):
        repository = await self.get_repository(obj_type)
        await repository.delete(id)

    async def get(self, id, obj_type):
        repository = await self.get_repository(obj_type)
        response = await repository.get(id)
        return response

    async def update(self, model: AbstractBaseEntity):
        repository = await self.get_repository(type(model))
        response = await repository.update(model)
        return response


class AbstractLinkUnitOfWork(ABC):

    repository: AbstractLinkRepository

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError
    
    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

    
class LinkUnitOfWork(AbstractLinkUnitOfWork):

    def __init__(self, reposiotry: AbstractLinkRepository, session_factory: AsyncSession):
        self.session_factory = session_factory
        self.repository = reposiotry

    async def __aenter__(self):
        self.session = await self.session_factory()
        self.repository = self.repository(self.session)
        return await super().__aenter__()
    
    async def __aexit__(self, *args):
        await super().__aexit__()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


