from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update

from src.archive.core import AbstractRepository
from src.archive.domains.document import Document
from .converter import dict_to_document, document_to_dict


class DocumentRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: Document) -> Document:
        data = document_to_dict(model=model)
        res = await self.session.execute(insert(Document).returning(Document), data)
        
        document = dict_to_document(res.scalars().first())
        return document

    async def get(self, id: int) -> Document:
        res = await self.session.execute(select(Document).filter_by(id=id))

        document = dict_to_document(res.scalars().first())
        return document

    async def get_list(self) -> list[Document]:
        results = await self.session.execute(select(Document))
        results = results.scalars().all()

        return [dict_to_document(res) for res in results]

    async def update(self, id: int, data: Document) -> Document:
        data = document_to_dict(data)

        res = await self.session.execute(update(Document).filter_by(id=id).returning(Document), data)

        document = dict_to_document(res.scalars().first())
        return document

    async def delete(self, id: int):
        await self.session.execute(delete(Document).filter_by(id=id))