import os

from typing import List, Dict
from pydantic import BaseModel

from src.archive.config import SAVE_FILES_URL
from src.archive.core import AbstractUnitOfWork, AbstractUnitOfWork2
from src.archive.domains.document import PhonoDocument


class PhonoDocumentService:

    async def create_document(
            self,
            files: Dict[str, bytes],
            data: BaseModel,
            uow: AbstractUnitOfWork,
    ) -> PhonoDocument:

        document = PhonoDocument(
            file_urls=list(files.keys()),
            author=data.author,
            dating=data.dating,
            place_of_creating=data.place_of_creating,
            genre=data.genre,
            brief_summary=data.brief_summary,
            addressee=data.addressee,
            cypher=data.cypher,
            lang=data.lang,
            storage_media=data.storage_media
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
        uow: AbstractUnitOfWork2,
        files: List[str] = None,
    ) -> PhonoDocument:

        async with uow as uow:
            document = await uow.get(id, PhonoDocument)
            document.remove_url_files_from_files(files)

            document = await uow.update(model=document)
            await uow.commit()

        for file_url in files:
            try:
                os.remove(SAVE_FILES_URL+file_url)
            except FileNotFoundError:
                pass


    async def update_document(
            self,
            id: int,
            data: BaseModel,
            files: Dict[str, bytes] | None,
            uow: AbstractUnitOfWork,
    ) -> PhonoDocument:

        async with uow as uow:
            document = await uow.repository.get(id=id)
            old_file_urls = document.file_urls
            document.update(
                new_file_urls = list(files.keys()) if files else None,
                new_author = data.author,
                new_dating = data.dating,
                new_place_of_creating = data.place_of_creating,
                new_genre = data.genre,
                new_brief_summary = data.brief_summary,
                new_addressee = data.addressee,
                new_cypher = data.cypher,
                new_lang = data.lang,
                new_storage_media = data.storage_media
            )
            document = await uow.repository.update(model=document)
            await uow.commit()
    
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

