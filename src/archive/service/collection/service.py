import re

from pydantic import BaseModel
from uuid import uuid4, UUID
from fpdf import FPDF
from sqlalchemy import delete

from src.archive.core import AbstractUnitOfWork, AbstractCacheService
from src.archive.core.unit_of_work import AbstractLinkUnitOfWork, AbstractUnitOfWork2
from src.archive.domains.collection import Collection
from src.archive.config import EDITING_COLLECTION_SESSION_EXPIRE_S, SAVE_FILES_URL
from src.archive.adapters import PDFAdapter
from src.archive.domains.notification import CollectionNotification
from src.archive.domains.user import Role
from src.archive.domains.user_link import SciCouncilGroupCollectionLink, RedactorGroupCollectionLink
from src.archive.domains.collection_comment import CollectionComment


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

.pdf-redactor-page-tools{
    display: none;
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

.left_parPosition{
	text-align: justify;
}

.central_parPosition{
	margin-left: auto;
	margin-right: auto;
	text-align: center;
}

.right_parPosition{
	text-align: right;
}

input[type="number"] {
	width: 35px;
	height: 25px;
	font-size: 14px;
	color: #333;
	border: 2px solid #ccc;
	border-radius: 4px;
	background-color: #f9f9f9;
	transition: border-color 0.3s, box-shadow 0.3s;
	text-align: center;
}

input[type="number"]:focus {
	border-color: #0066cc;
	box-shadow: 0 0 5px rgba(0, 102, 204, 0.5);
	outline: none;
}

input[type="number"]::-webkit-inner-spin-button, 
input[type="number"]::-webkit-outer-spin-button {
	-webkit-appearance: none;
	margin: 0;
}

input[type="number"] {
	-moz-appearance: textfield;
}


p{
	margin-top: 5px;
	margin-bottom:0;
}

.pdf-redactor-page-number{
	position: relative;
	margin-left: auto;
	margin-right: auto;
	text-align: center;

	top: 45px; /* padding-bottom от исходного padding */
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
        pdf.output(f"{SAVE_FILES_URL}collections/{file_url}")
        with open(f"{SAVE_FILES_URL}collections/{html_url}", "w") as html_file:
            html_file.write(start_html_content)

        return collection
   
    async def connect_to_editing(
           self,
           user_id: str,
           document_id: str,
           cache_service: AbstractCacheService
    ):
        if cache_service.exists(document_id):
            edit_user_id = cache_service.get(document_id)
            if edit_user_id != user_id:
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
                    new_title = data.title,
                )
                collection = await uow.repository.update(model=collection)
            await uow.commit()

        with open(f"{SAVE_FILES_URL}collections/{collection.html_url}", 'r', encoding='utf-8') as file:
            html_content = file.read()

        pattern = re.compile(r'(?<=</head>)(.*?)(?=</html>)', re.DOTALL)

        updated_html_content = re.sub(pattern, data.html_data, html_content)

        with open(f"{SAVE_FILES_URL}collections/{collection.html_url}", 'w', encoding='utf-8') as file:
            file.write(updated_html_content)

        PDFAdapter.html_to_pdf(html_code=updated_html_content, path=f"{SAVE_FILES_URL}collections/{collection.file_url}") 

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


    async def bind_user_to_collection_group(
            self,
            coll_id: str,
            user_data: BaseModel,
            uow: AbstractUnitOfWork2,   
    ):
        notification = CollectionNotification(
            collection_id=coll_id,
            user_id=user_data.id,
        )
        coll_comment = CollectionComment(
            collection_id=coll_id,
            user_id=user_data.id,
            text=""
        )
        try:
            user = None
            if user_data.role == Role.ScientificCouncil.value:
                user = SciCouncilGroupCollectionLink(
                    collection_id=coll_id,
                    scientific_council_id=user_data.id
                )
            elif user_data.role == Role.RedactorUser.value:
                user = RedactorGroupCollectionLink(
                    collection_id=coll_id,
                    redactor_id=user_data.id
                )
            async with uow as uow:
                notification = await uow.add(notification)
                comment = await uow.add(coll_comment)
                link_id = await uow.add(user)
                await uow.commit()
        except ValueError:
            raise ValueError("User doen't have access to scientific council group")

    async def del_bind_user_from_collection_group(
            self,
            coll_id: str,
            user_data: BaseModel,
            uow: AbstractUnitOfWork2
    ):
        try:
            async with uow as uow:
                if user_data.role == Role.ScientificCouncil.value:
                    repo = await uow.get_repository(SciCouncilGroupCollectionLink)       
                elif user_data.role == Role.RedactorUser.value:
                    repo = await uow.get_repository(RedactorGroupCollectionLink)
                comment_repo = await uow.get_repository(CollectionComment)
                await comment_repo.delete_by_coll_and_user_id(coll_id, user_data.id)
                await repo.delete_by_coll_and_user_id(coll_id, user_data.id)
                await uow.commit()
        except ValueError:
            raise ValueError("User don't have access")


    async def approve_by_sci_user(
            self,
            coll_id: str,
            user_id: str,
            approve: bool,
            uow: AbstractUnitOfWork
    ):
        async with uow as uow:
            collection = await uow.repository.get(id=coll_id)
            collection._is_approved = False
            await uow.link_repository.update(obj_id=coll_id, related_obj_id=user_id, approve=approve, user_role=Role.ScientificCouncil.value)
            await uow.repository.update(model=collection)
            await uow.commit()


    async def approve_by_admin_redactor_users(
        self,
        coll_id: str,
        user_id: str,
        user_role: str,
        approve: bool,
        sci_group: BaseModel,
        uow: AbstractUnitOfWork
    ):
        async with uow as uow:
            is_user_in_group = False
            collection = await uow.repository.get(id=coll_id)
            if user_role == Role.RedactorUser.value:
                is_user_in_group = await uow.link_repository.exist(obj_id=coll_id, related_obj_id=user_id, user_role=user_role)
            elif user_role == Role.AdminUser.value:
                is_user_in_group = str(collection.author_id) == user_id
 
        for sci in sci_group:
            if sci.is_approved == False:
                raise ValueError("Collection not approved by all scientific Council")

        # if is_user_in_group == False:
        #     print("nono")
        #     raise ValueError("Access denied")

        async with uow as uow:
            collection._is_approved = approve
            collection = await uow.repository.update(model=collection)
            await uow.commit()

        return collection


    async def set_isbn_link(
        self,
        coll_id: str,
        data: BaseModel,
        uow: AbstractUnitOfWork
    ):
        async with uow as uow:
            collection = await uow.repository.get(id=coll_id)
            collection.set_isbn_link(data.isbn_link)
            collection = await uow.repository.update(model=collection)
            await uow.commit()
    
    
    async def delete_collection(
        self,
        coll_id: str,
        user_id: str,
        uow: AbstractUnitOfWork2
    ):
        async with uow as uow:
            coll = await uow.get(coll_id, Collection)
            if str(coll.author_id) != user_id:
                raise ValueError("Access denied")
            await uow.delete(coll_id, Collection)
            await uow.commit()
