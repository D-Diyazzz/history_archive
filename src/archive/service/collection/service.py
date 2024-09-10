from pydantic import BaseModel
from uuid import uuid4, UUID
from fpdf import FPDF

from src.archive.core import AbstractUnitOfWork, AbstractCacheService
from src.archive.domains.collection import Collection
from src.archive.config import EDITING_COLLECTION_SESSION_EXPIRE_S


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
           user_id: UUID,
           document_id: UUID,
           cache_service: AbstractCacheService
    ):
       if cache_service.exists(document_id):
           raise ValueError(f"Document with id {document_id} already editing")

       cache_service.set(document_id, user_id, EDITING_COLLECTION_SESSION_EXPIRE_S)
