from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete

from src.archive.core import AbstractRepository
from src.archive.domains.Form_collection import FormCollection


class FormCollectionRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: FormCollection) -> FormCollection:
        res = await self.session.execute(insert(FormCollection).returning(FormCollection), {"name": model.get_name()})
        return res.scalars().first()

    async def get(self, id) -> FormCollection:
        res = await self.session.execute(select(FormCollection).filter_by(id=id))
        return res.scalars().first()
    
    async def get_list(self) -> list[FormCollection]:
        res = await self.session.execute(select(FormCollection))
        return res.scalars().all()
    
    async def delete(self, id):
        await self.session.execute(delete(FormCollection).filter_by(id=id))