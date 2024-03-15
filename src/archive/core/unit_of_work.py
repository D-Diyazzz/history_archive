from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from src.archive.core import AbstractBaseEntity, AbstractRepository


class AbstractUnitOfWork(ABC):
    repository: AbstractRepository

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

    def __init__(self, reposiotry: AbstractRepository, session_factory: AsyncSession):
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
    