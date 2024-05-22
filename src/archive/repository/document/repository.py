from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update

from src.archive.core import AbstractRepository
from src.archive.domains.document import Document
from .converter import dict_to_document, document_to_dict, search_data_to_dict
from .statements import insert_document, insert_search_data, select_document_by_id, select_document, update_document, update_search_data, delete_search_data


class DocumentRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: Document) -> Document:
        search_data_dict = search_data_to_dict(model=model)

        search_data_id = await self.session.execute(
            insert_search_data,
            search_data_dict
        )

        search_data_id = search_data_id.scalars().first()
        model._search_data._id = search_data_id
        document_data_dict = document_to_dict(model=model)

        id = await self.session.execute(
            insert_document,
            document_data_dict
        )

        model._id = id.scalars().first()

        return model

    async def get(self, id: int) -> Document:
        res = await self.session.execute(
            select_document_by_id,
            {"id": id}
        )
        data = res.one()
        document = dict_to_document(data=data)
        return document

    async def get_list(self) -> list[Document]:
        results = await self.session.execute(
            select_document
        )
        results = results.all()

        return [dict_to_document(res) for res in results]

    async def update(self, model: Document) -> Document:
        search_data_dict = search_data_to_dict(model=model)
        search_data_dict["id"] = model.search_data.id
        data = document_to_dict(model=model)
        data["id"] = model.id

        await self.session.execute(
            update_search_data,
            search_data_dict
        )

        await self.session.execute(
            update_document,
            data
        )

        return model

    async def delete(self, search_data_id: int):
        await self.session.execute(
            delete_search_data,
            {
                "id": search_data_id
            }
        )

    