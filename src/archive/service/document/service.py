from pydantic import BaseModel

from src.archive.core import AbstractUnitOfWork
from src.archive.domains.document import Document


class DocumentService:

    async def create_document(
            self,
            file: bytes,
            data: BaseModel,
            uow: AbstractUnitOfWork,
    ) -> Document:

        document = Document(
            file_url=data.file_url,
            author=data.author,
            dating=data.dating,
            place_of_creating=data.place_of_creating,
            variety=data.variety,
            addressee=data.addressee,
            brief_content=data.brief_content,
            case_prod_number=data.case_prod_number,
            main_text=data.main_text,
            search_data=data.search_data,
        )

        async with uow as uow:
            document = await uow.repository.add(document)
            await uow.commit()
        
        with open(f"files/{data.file_url}", "wb") as buffer:
            buffer.write(file)
        
        return document

    async def get_document(
            self,
            id: int,
            uow: AbstractUnitOfWork,
    ) -> Document:
        
        async with uow as uow:
            document = await uow.repository.get(id=id)
        
        return document

    async def get_list_document(
            self,
            uow: AbstractUnitOfWork,
    ) -> list[Document]:
        
        async with uow as uow:
            documents = await uow.repository.get_list()

        return documents

    async def update_document(
            self,
            id: int,
            data: BaseModel,
            file: bytes | None,
            uow: AbstractUnitOfWork,
    ) -> Document:
        
        document = Document(
            file_url=data.file_url,
            title=data.title,
            heading=data.heading,
            author=data.author,
            description_content=data.description_content,
            dating=data.dating,
            legends=data.legends,
            format_doc=data.format_doc,
            color_palette=data.color_palette,
            resolution=data.resolution,
            compression=data.compression,
            scanner_model=data.scanner_model,
        )

        async with uow as uow:
            document = await uow.repository.update(id=id, data=document)
            await uow.commit()

        if file:
            with open(f"files/{data.file_url}", "wb") as buffer:
                buffer.write(file)
        
        return document

    async def delete_document(
            self,
            id: int,
            uow: AbstractUnitOfWork,
    ):
        async with uow as uow:
            await uow.repository.delete(id=id)
            await uow.commit()