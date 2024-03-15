from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete

from src.archive.core import AbstractRepository
from src.archive.domains.Method_collection import MethodCollection


class MethodCollectionRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: MethodCollection) -> MethodCollection:
        res = await self.session.execute(insert(MethodCollection).returning(MethodCollection), {"name": model.get_name()})
        return res.scalars().first()

    async def get(self, id) -> MethodCollection:
        res = await self.session.execute(select(MethodCollection).filter_by(id=id))
        return res.scalars().first()
    
    async def get_list(self) -> list[MethodCollection]:
        res = await self.session.execute(select(MethodCollection))
        return res.scalars().all()
    
    async def delete(self, id):
        await self.session.execute(delete(MethodCollection).filter_by(id=id))