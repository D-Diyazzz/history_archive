from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete

from src.archive.core import AbstractRepository
from src.archive.domains.Class_collection import ClassCollection


class ClassCollectionRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: ClassCollection) -> ClassCollection:
        res = await self.session.execute(insert(ClassCollection).returning(ClassCollection), {"name": model.get_name()})
        return res.scalars().first()

    async def get(self, id) -> ClassCollection:
        res = await self.session.execute(select(ClassCollection).filter_by(id=id))
        return res.scalars().first()
    
    async def get_list(self) -> list[ClassCollection]:
        res = await self.session.execute(select(ClassCollection))
        return res.scalars().all()
    
    async def delete(self, id):
        await self.session.execute(delete(ClassCollection).filter_by(id=id))