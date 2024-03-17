from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete

from src.archive.core import AbstractRepository
from src.archive.domains.Type import TypeCollection


class TypeRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: TypeCollection) -> TypeCollection:
        res = await self.session.execute(insert(TypeCollection).returning(TypeCollection), {"name": model.name})
        return res

    async def get(self, id) -> TypeCollection:
        res = await self.session.execute(select(TypeCollection).filter_by(id=id))
        return res.scalars().first()
    
    async def get_list(self) -> list[TypeCollection]:
        res = await self.session.execute(select(TypeCollection))
        return res.scalars().all()
    
    async def delete(self, id):
        await self.session.execute(delete(TypeCollection).filter_by(id=id))