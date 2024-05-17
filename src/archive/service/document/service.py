import os

from pydantic import BaseModel

from src.archive.core import AbstractUnitOfWork
from src.archive.domains.document import Document, SearchData


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
            search_data=SearchData(
                cypher=data.search_data.cypher,
                fund=data.search_data.fund,
                inventory=data.search_data.inventory,
                case=data.search_data.case,
                leaf=data.search_data.leaf,
                authenticity=data.search_data.authenticity,
                lang=data.search_data.lang,
                playback_method=data.search_data.playback_method,
                other=data.search_data.other if data.search_data.other else None
            ),
        )

        async with uow as uow:
            document = await uow.repository.add(document)
            await uow.commit()
        
        with open(f"files/{data.file_url}", "wb") as buffer:
            buffer.write(file)
        
        return document


    async def update_document(
            self,
            id: int,
            data: BaseModel,
            file: bytes | None,
            uow: AbstractUnitOfWork,
    ) -> Document:

        async with uow as uow:
            document = await uow.repository.get(id=id)
            search_data = document.search_data
            search_data.update(
                new_cypher = data.search_data.cypher,
                new_fund=data.search_data.fund,
                new_inventory=data.search_data.inventory,
                new_case=data.search_data.case,
                new_leaf=data.search_data.leaf,
                new_authenticity=data.search_data.authenticity,
                new_lang=data.search_data.lang,
                new_playback_method=data.search_data.playback_method,
                new_other=data.search_data.other
            )
            old_file_url = f"files/{document.file_url}"
            document.update(
                new_file_url = data.file_url,
                new_author = data.author,
                new_dating = data.dating,
                new_place_of_creating = data.place_of_creating,
                new_variety = data.variety,
                new_addressee = data.addressee,
                new_brief_content = data.brief_content,
                new_case_prod_number = data.case_prod_number,
                new_main_text = data.main_text,
                updated_search_data = search_data
            )
            document = await uow.repository.update(model=document)
            await uow.commit()

        if old_file_url != document.file_url:
            os.rename(old_file_url, f"files/{document.file_url}")

        if file:
            with open(f"files/{document.file_url}", "wb") as buffer:
                buffer.write(file)
        
        return document

    async def delete_document(
            self,
            id: int,
            uow: AbstractUnitOfWork,
    ):
        async with uow as uow:
            document = await uow.repository.get(id=id)
            await uow.repository.delete(id=document.id)
            await uow.commit()

        os.remove(f"files/{document.file_url}")