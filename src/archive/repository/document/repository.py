from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update

from src.archive.core import AbstractRepository
from src.archive.domains.document import Document
from .converter import dict_to_document, document_to_dict
from .statements import insert_document, select_document_by_id, select_document, update_document, update_search_data, delete_document


class DocumentRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: Document) -> Document:
        data = document_to_dict(model=model)

        id = await self.session.execute(
            insert_document,
            data
        )

        model._id = id

        return model

    async def get(self, id: int) -> Document:
        res = await self.session.execute(
            select_document_by_id,
            {"id": id}
        )
        document = dict_to_document(data=res.scalars().first())
        return document

    async def get_list(self) -> list[Document]:
        results = await self.session.execute(
            select_document
        )
        results = results.scalars().all()

        return [dict_to_document(res) for res in results]

    async def update(self, model: Document) -> Document:
        data = document_to_dict(model=model)

        await self.session.execute(
            update_search_data,
            {
                "id": model.search_data.id,
                "search_data_cypher": model.search_data.cypher,
                "search_data_fund": model.search_data.fund,
                "search_data_inventory": model.search_data.inventory,
                "search_data_case": model.search_data.case,
                "search_data_leaf": model.search_data.leaf,
                "search_data_authenticity": model.search_data.authenticity,
                "search_data_lang": model.search_data.lang,
                "search_data_playback_method": model.search_data.playback_method,
                "search_data_other": model.search_data.other
            }
        )

        await self.session.execute(
            update_search_data,
            data
        )

        return model

    async def delete(self, id: int):
        await self.session.execute(delete(Document).filter_by(id=id))