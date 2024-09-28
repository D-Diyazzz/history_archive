from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from src.archive.core import AbstractBaseEntity, AbstractRepository, AbstractLinkRepository


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


