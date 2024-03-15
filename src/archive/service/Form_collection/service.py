from pydantic import BaseModel

from src.archive.core import AbstractUnitOfWork
from src.archive.domains.Form_collection import FormCollection


class FormCollectionService:

    async def create_form_collection(
            self,
            data: BaseModel,
            uow: AbstractUnitOfWork,
    ) -> FormCollection:
        
        form_collection = FormCollection(
            name=data.name,
        )

        async with uow as uow:
            form_collection = await uow.repository.add(form_collection)
            await uow.commit()
        
        return form_collection
    

    async def get_list_form_collection(
            self,
            uow: AbstractUnitOfWork,
    ) -> list[FormCollection]:
        
        async with uow as uow:
            list_form_collection = await uow.repository.get_list()
            list_form_collection = [
                FormCollection(
                    id=form_collection.id,
                    name=form_collection.name,
                ) for form_collection in list_form_collection
            ]

        return list_form_collection
    

    async def get_form_collection(
            self,
            data: id,
            uow: AbstractUnitOfWork,
    ) -> FormCollection:
        
        async with uow as uow:
            form_collection = await uow.repository.get(id=data)
            form_collection = FormCollection(
                id=form_collection.id,
                name=form_collection.name
            )

        return form_collection
    

    async def delete_form_collection(
            self,
            data: id,
            uow: AbstractUnitOfWork,
    ):
        
        async with uow as uow:
            await uow.repository.delete(id=data)
            await uow.commit()