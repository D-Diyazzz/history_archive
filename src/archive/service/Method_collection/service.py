from pydantic import BaseModel

from src.archive.core import AbstractUnitOfWork
from src.archive.domains.Method_collection import MethodCollection


class MethodCollectionService:

    async def create_method_collection(
            self,
            data: BaseModel,
            uow: AbstractUnitOfWork,
    ) -> MethodCollection:
        
        method_collection = MethodCollection(
            name=data.name,
        )

        async with uow as uow:
            method_collection = await uow.repository.add(method_collection)
            await uow.commit()
        
        return method_collection
    

    async def get_list_method_collection(
            self,
            uow: AbstractUnitOfWork,
    ) -> list[MethodCollection]:
        
        async with uow as uow:
            list_method_collection = await uow.repository.get_list()
            list_method_collection = [
                MethodCollection(
                    id=method_collection.id,
                    name=method_collection.name,
                ) for method_collection in list_method_collection
            ]

        return list_method_collection
    

    async def get_method_collection(
            self,
            data: id,
            uow: AbstractUnitOfWork,
    ) -> MethodCollection:
        
        async with uow as uow:
            method_collection = await uow.repository.get(id=data)
            method_collection = MethodCollection(
                id=method_collection.id,
                name=method_collection.name
            )

        return method_collection
    

    async def delete_method_collection(
            self,
            data: id,
            uow: AbstractUnitOfWork,
    ):
        
        async with uow as uow:
            await uow.repository.delete(id=data)
            await uow.commit()