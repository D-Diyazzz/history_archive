from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete

from src.archive.core import AbstractRepository
from src.archive.domains.Type import Type


class TypeRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: Type) -> Type:
        res = await self.session.execute(insert(Type).returning(Type), {"name": model.name})
        return res

    async def get(self, id) -> Type:
        res = await self.session.execute(select(Type).filter_by(id=id))
        return res.scalars().first()
    
    async def get_list(self) -> list[Type]:
        res = await self.session.execute(select(Type))
        return res.scalars().all()
    
    async def delete(self, id):
        await self.session.execute(delete(Type).filter_by(id=id))