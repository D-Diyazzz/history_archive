from pydantic import BaseModel

from src.archive.core import AbstractUnitOfWork
from src.archive.domains.Type import Type


class TypeServices:

    async def create_type(
            self,
            data: BaseModel,
            uow: AbstractUnitOfWork
    ) -> Type:
        type_collection = Type(
            name=data.name,
        )

        async with uow as uow:
            type_response = await uow.repository.add(type_collection)
            await uow.commit()

        return type_response.first()[0]
    

    async def get_list_of_type(
            self,
            uow: AbstractUnitOfWork,
    ) -> list[Type]:
        async with uow as uow:
            list_types = await uow.repository.get_list()
            list_types = [Type(id=type.id, name=type.name) for type in list_types]

        return list_types
    

    async def get_type_collection(
            self,
            data: id,
            uow: AbstractUnitOfWork,
    ) -> Type:
        async with uow as uow:
            type = await uow.repository.get(id=data)
            type = Type(id=type.id, name=type.name)
        return type

    
    async def delete_type_collection(
            self,
            data: id,
            uow: AbstractUnitOfWork,
    ):
        async with uow as uow:
            await uow.repository.delete(id=data)
            await uow.commit()

        