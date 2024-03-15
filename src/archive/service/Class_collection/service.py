from pydantic import BaseModel

from src.archive.core import AbstractUnitOfWork
from src.archive.domains.Class_collection import ClassCollection


class ClassCollectionService:

    async def create_class_collection(
            self,
            data: BaseModel,
            uow: AbstractUnitOfWork,
    ) -> ClassCollection:
        class_collection = ClassCollection(
            name=data.name,
        )

        async with uow as uow:
            class_collection = await uow.repository.add(class_collection)
            await uow.commit()
        
        return class_collection
    

    async def get_list_class_collection(
            self,
            uow: AbstractUnitOfWork,
    ) -> list[ClassCollection]:
        
        async with uow as uow:
            list_class_collection = await uow.repository.get_list()
            list_class_collection = [
                ClassCollection(
                    id=class_collection.id,
                    name=class_collection.name,
                ) for class_collection in list_class_collection
            ]

        return list_class_collection


    async def get_class_collection(
            self,
            data: id,
            uow: AbstractUnitOfWork,
    ) -> ClassCollection:
        
        async with uow as uow:
            class_collectino = await uow.repository.get(id=data)
            class_collectino = ClassCollection(
                id=class_collectino.id,
                name=class_collectino.name,
            )

        return class_collectino
    

    async def delete_class_collection(
            self,
            data: id,
            uow: AbstractUnitOfWork,
    ):
        async with uow as uow:
            await uow.repository.delete(id=data)
            await uow.commit()