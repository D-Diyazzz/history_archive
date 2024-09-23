import re

from pydantic import BaseModel
from uuid import uuid4, UUID
from fpdf import FPDF

from src.archive.core import AbstractUnitOfWork, AbstractCacheService
from src.archive.core.unit_of_work import AbstractLinkUnitOfWork
from src.archive.domains.collection import Collection
from src.archive.config import EDITING_COLLECTION_SESSION_EXPIRE_S
from src.archive.adapters import PDFAdapter
from src.archive.domains.notification import CollectionNotification
from src.archive.domains.user import Role


start_html_content = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <style>

@page {
    margin: 0;  /* Убираем отступы страницы */
    padding: 0; /* Убираем внутренние отступы страницы */
}

html, body {
    margin: 0;
    padding: 0;
    border: none; /* Убираем любые границы */
    outline: none; /* Убираем обводку */
    background-color: red;
    
}

.pdf-redactor-page {
    width: 794px;
    height: 1123px;
    background-color: white;
    margin-left: 0;
    margin-right: 0;
    border: 1px solid black;  /* Убираем границу */
    outline: none; /* Убираем обводку */
    word-wrap: break-word;
    box-sizing: border-box;
    padding:93px;
}

.pdf-redactor-page-edit {
width: 100%;
    outline: none;
    word-wrap: break-word;
    word-break: break-word;
    box-sizing: border-box;
    font-family: 'Times New Roman', Times, serif;
    border: none; /* Убираем границу */
    outline: none; /* Убираем обводку */
}

.pdf-redactor-page-edit p{
	caret-color: black;
}

.pdf-redactor-page-edit p span{
	caret-color: black;
}

.bold{
	font-weight: bold;
}

.italic{
	font-style: italic;
}

.central-text-position{
	margin-left: auto;
	margin-right: auto;
	text-align: center;
}

.right-text-position{
	text-align: right;
}

p{
	margin-top: 5px;
	margin-bottom:0;
}

    </style>
</head>

</html>
'''


class CollectionService: 

    async def create_collection(
            self,
            author_id: UUID,
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
            author_id=author_id,
        )

        async with uow as uow:
            collection = await uow.repository.add(collection)
            await uow.commit()
        

        pdf = FPDF()
        pdf.add_page()
        pdf.output(f"files/collections/{file_url}")
        with open(f"files/collections/{html_url}", "w") as html_file:
            html_file.write(start_html_content)

        return collection
   
    async def connect_to_editing(
           self,
           user_id: str,
           document_id: str,
           cache_service: AbstractCacheService
    ):
       if cache_service.exists(document_id):
           raise ValueError(f"Document with id {document_id} already editing")

       cache_service.set(document_id, user_id, EDITING_COLLECTION_SESSION_EXPIRE_S)


    async def edit_collection(
            self,
            user_id: str,
            document_id: str,
            data: BaseModel,
            cache_service: AbstractCacheService,
            uow: AbstractUnitOfWork,
    ):
        async with uow as uow:
            collection = await uow.repository.get(id=document_id)
            if collection.theme != data.theme or collection.title != data.title:
                collection.update(
                    new_theme = data.theme,
                    new_title = data.title
                )
                print(collection.__dict__)
                collection = await uow.repository.update(model=collection)
            await uow.commit()

        with open(f"files/collections/{collection.html_url}", 'r', encoding='utf-8') as file:
            html_content = file.read()

        pattern = re.compile(r'(?<=</head>)(.*?)(?=</html>)', re.DOTALL)

        updated_html_content = re.sub(pattern, data.html_data, html_content)

        with open(f"files/collections/{collection.html_url}", 'w', encoding='utf-8') as file:
            file.write(updated_html_content)

        PDFAdapter.html_to_pdf(html_code=updated_html_content, path=f"files/collections/{collection.file_url}") 

        cache_service.set(document_id, user_id, EDITING_COLLECTION_SESSION_EXPIRE_S)


    async def pin_document(
            self,
            id: str,
            data: BaseModel,
            uow: AbstractLinkUnitOfWork,
    ):
        async with uow as uow:
            id = await uow.repository.add(obj_id=id, related_obj_id=data.doc_id, doc_type=data.doc_type)
            await uow.commit()

        return id

    async def delete_document_link(
            self,
            id: str,
            data: BaseModel,
            uow: AbstractLinkUnitOfWork
    ):
        async with uow as uow:
            await uow.repository.delete(obj_id=id, related_obj_id=data.doc_id, doc_type=data.doc_type)
            await uow.commit()


    async def bind_user_to_scientific_group(
            self,
            coll_id: str,
            user_data: BaseModel,
            uow: AbstractUnitOfWork,    
    ):
        if user_data.role != Role.ScientificCouncil.value:
            raise ValueError("User doen't have access to scientific council group")
        notification = CollectionNotification(
            collection_id=coll_id,
            user_id=user_data.id,
        )

        async with uow as uow:
            notification = await uow.repository.add(notification)
            link_id = await uow.link_repository.add(obj_id=coll_id, related_obj_id=user_data.id)
            await uow.commit()


