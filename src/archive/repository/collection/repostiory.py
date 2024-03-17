from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update

from src.archive.core import AbstractRepository
from src.archive.domains.collection import Collection
from src.archive.domains.Type import TypeCollection
from src.archive.domains.Class_collection import ClassCollection
from src.archive.domains.Form_collection import FormCollection
from src.archive.domains.Method_collection import MethodCollection
from .converter import collection_to_dict, dict_to_collection


class CollectionRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: Collection) -> Collection:
        data = collection_to_dict(model)
        res = await self.session.execute(insert(Collection).returning(Collection), data)
        res = res.scalars().first()

        type_coll = await self.session.execute(select(TypeCollection).filter_by(id=res.type_id))
        class_coll = await self.session.execute(select(ClassCollection).filter_by(id=res.class_id))
        format_coll = await self.session.execute(select(FormCollection).filter_by(id=res.format_id))
        method_coll = await self.session.execute(select(MethodCollection).filter_by(id=res.method_id))

        type_coll = type_coll.scalars().first()
        class_coll = class_coll.scalars().first()
        format_coll = format_coll.scalars().first()
        method_coll = method_coll.scalars().first()

        collection = dict_to_collection(res, type_coll, class_coll, format_coll, method_coll)

        return collection
    
    async def get(self, id: int) -> Collection:
        res = await self.session.execute(select(Collection).filter_by(id=id))
        res = res.scalars().first()

        type_coll = await self.session.execute(select(TypeCollection).filter_by(id=res.type_id))
        class_coll = await self.session.execute(select(ClassCollection).filter_by(id=res.class_id))
        format_coll = await self.session.execute(select(FormCollection).filter_by(id=res.format_id))
        method_coll = await self.session.execute(select(MethodCollection).filter_by(id=res.method_id))

        type_coll = type_coll.scalars().first()
        class_coll = class_coll.scalars().first()
        format_coll = format_coll.scalars().first()
        method_coll = method_coll.scalars().first()

        collection = dict_to_collection(res, type_coll, class_coll, format_coll, method_coll)

        return collection

    async def get_list(self) -> list[Collection]:
        results = await self.session.execute(select(Collection))
        results = results.scalars().all()

        collections = []

        for res in results:
            type_coll = await self.session.execute(select(TypeCollection).filter_by(id=res.type_id))
            class_coll = await self.session.execute(select(ClassCollection).filter_by(id=res.class_id))
            format_coll = await self.session.execute(select(FormCollection).filter_by(id=res.format_id))
            method_coll = await self.session.execute(select(MethodCollection).filter_by(id=res.method_id))

            type_coll = type_coll.scalars().first()
            class_coll = class_coll.scalars().first()
            format_coll = format_coll.scalars().first()
            method_coll = method_coll.scalars().first()

            collection = dict_to_collection(res, type_coll, class_coll, format_coll, method_coll)
            collections.append(collection)
        
        return collections

    async def update(self, id:int, data: Collection):
        data = collection_to_dict(data)

        res = await self.session.execute(update(Collection).filter_by(id=id).returning(Collection), data)
        res = res.scalars().first()

        type_coll = await self.session.execute(select(TypeCollection).filter_by(id=res.type_id))
        class_coll = await self.session.execute(select(ClassCollection).filter_by(id=res.class_id))
        format_coll = await self.session.execute(select(FormCollection).filter_by(id=res.format_id))
        method_coll = await self.session.execute(select(MethodCollection).filter_by(id=res.method_id))

        type_coll = type_coll.scalars().first()
        class_coll = class_coll.scalars().first()
        format_coll = format_coll.scalars().first()
        method_coll = method_coll.scalars().first()

        collection = dict_to_collection(res, type_coll, class_coll, format_coll, method_coll)

        return collection


    async def delete(self, id: int):
        await self.session.execute(delete(Collection).filter_by(id=id))