import os

from typing import List, Dict
from pydantic import BaseModel

from src.archive.config import SAVE_FILES_URL
from src.archive.core import AbstractUnitOfWork
from src.archive.domains.document import Document, SearchData


class DocumentService:

    async def create_document(
            self,
            files: Dict[str, bytes],
            data: BaseModel,
            uow: AbstractUnitOfWork,
    ) -> Document:

        document = Document(
            file_urls=list(files.keys()),
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
        
        if files:
            for file_url, file_bytes in files.items():
                with open(SAVE_FILES_URL+file_url, "wb") as buffer:
                    buffer.write(file_bytes)
        
        return document

    
    async def remove_file_in_document(
            self,
            id: int,
            files: List[str],
            uow: AbstractUnitOfWork,
    ) -> Document:
        
        async with uow as uow:
            document = await uow.repository.get(id=id)
            document.remove_url_files_from_files(files)

            document = await uow.repository.update(model=document)
            await uow.commit()
        
        for file_url in files:
            try:
                os.remove(SAVE_FILES_URL + file_url)
            except FileNotFoundError:
                pass

        return document


    async def update_document(
            self,
            id: int,
            data: BaseModel,
            files: Dict[str, bytes] | None,
            uow: AbstractUnitOfWork,
    ) -> Document:

        async with uow as uow:
            document = await uow.repository.get(id=id)
            document.search_data.update(
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
            document.update(
                new_file_urls = list(files.keys()) if files else None,
                new_author = data.author,
                new_dating = data.dating,
                new_place_of_creating = data.place_of_creating,
                new_variety = data.variety,
                new_addressee = data.addressee,
                new_brief_content = data.brief_content,
                new_case_prod_number = data.case_prod_number,
                new_main_text = data.main_text,
            )
            document = await uow.repository.update(model=document)
            await uow.commit()
    

        # if old_file_url != document.file_url:
        #     os.rename(old_file_url, f"files/{document.file_url}")

        if files:
            for file_url, file_bytes in files.items():
                with open(SAVE_FILES_URL+file_url, "wb") as buffer:
                    buffer.write(file_bytes)
        
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

        file_urls = document.file_urls
        for file_url in file_urls:
            try:
                os.remove(SAVE_FILES_URL+file_url)
            except FileNotFoundError:
                pass
