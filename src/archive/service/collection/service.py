from pydantic import BaseModel
from uuid import uuid4

from src.archive.core import AbstractUnitOfWork
from src.archive.domains.collection import Collection


class CollectionService: 

    async def create_collection(
            self,
            data: BaseModel,
            uow: AbstractUnitOfWork,
    ) -> Collection:
        file_url = str(uuid4()) + ".pdf"
        html_url = str(uuid4()) + ".html"
        collection = Collection(
            file_url=file_url,
            html_url=html_url,
            theme=data.theme,
            title=data.title,
            author_id=data.author_id,
        )

        async with uow as uow:
            collection = await uow.repository.add(collection)
            await uow.commit()
        

        with open(f"files/collection/{file_url}", "w"):
            pass

        with open(f"files/collection/{html_url}", "w"):
            pass

        return collection
    
    async def get_collection(
            self,
            id: int,
            uow: AbstractUnitOfWork,
    ) -> Collection:
        
        async with uow as uow:
            colleciton = await uow.repository.get(id=id)

        return colleciton
    
    async def get_list_collection(
            self,
            uow: AbstractUnitOfWork,
    ) -> list[Collection]:
        
        async with uow as uow:
            collections = await uow.repository.get_list()
        
        return collections

    async def update_collection(
            self,
            id: int,
            data: BaseModel,
            file: bytes | None,
            uow: AbstractUnitOfWork,
    ) -> Collection:
        collection = Collection(
            file_url=data.file_url,
            theme=data.theme,
            purpose=data.purpose,
            task=data.task,
            type_coll=Type(
                id=data.type_coll_id,
                name=None
            ),
            class_coll=Class(
                id=data.class_coll_id,
                name=None
            ),
            format_coll=Format(
                id=data.format_coll_id,
                name=None
            ),
            method_coll=Method(
                id=data.method_coll_id,
                name=None
            ),
            preface=data.preface,
            note=data.note,
            indication=data.indication,
            intro_text=data.intro_text,
            recommendations=data.recommendations,
        )

        async with uow as uow:
            collection = await uow.repository.update(id=id, data=collection)
            await uow.commit()

        if file:
            with open(f"files/{data.file_url}", "wb") as buffer:
                buffer.write(file)

        return collection

    async def delete_collection(
            self,
            id: int,
            uow: AbstractUnitOfWork,
    ):
        async with uow as uow:
            await uow.repository.delete(id=id)
            await uow.commit()
        
