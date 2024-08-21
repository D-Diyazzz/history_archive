from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update

from src.archive.core import AbstractRepository
from src.archive.domains.collection import Collection
from .converter import collection_to_dict, dict_to_collection
from .statements import insert_collection, select_collection_by_id, update_collection, delete_collection, select_collection


class CollectionRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: Collection) -> Collection:
        data = collection_to_dict(model)
        
        id = await self.session.execute(
            insert_collection,
            data
        )

        model._id = id.scalars().first()

        return model
    
    async def get(self, id: int) -> Collection:
        res = await self.session.execute(
            select_collection_by_id,
            {"id": id}
        )
        
        collection = dict_to_collection(collection=res.one())

        return collection

    async def get_list(self) -> list[Collection]:
        res = await self.session.execute(
            select_collection
        )
        res = res.all()

        return [dict_to_collection(r) for r in res]

    async def update(self, model: Collection):
        data = collection_to_dict(data)
        
        await self.session.execute(
            update_collection,
            data
        )

        return model


    async def delete(self, id: int):
        await self.session.execute(
            delete_collection,
            {
                "id": id
            }
        ) 
