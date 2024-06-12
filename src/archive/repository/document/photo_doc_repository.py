from sqlalchemy.ext.asyncio import AsyncSession

from src.archive.core import AbstractRepository
from src.archive.domains.document import PhotoDocument
from .converter import dict_to_photo_document, photo_document_to_dict, search_data_to_dict
from .statements import (
    insert_photo_document,
    insert_search_data,
    select_photo_document_by_id,
    select_photo_document,
    update_photo_document,
    update_search_data,
    delete_search_data
)


class PhotoDocumentRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: PhotoDocument) -> PhotoDocument:
        search_data_dict = search_data_to_dict(model=model)

        search_data_id = await self.session.execute(
            insert_search_data,
            search_data_dict
        )

        search_data_id = search_data_id.scalars().first()
        model._search_data._id = search_data_id
        photo_document_data_dict = photo_document_to_dict(model=model)

        id = await self.session.execute(
            insert_photo_document,
            photo_document_data_dict
        )

        model._id = id.scalars().first()

        return model

    async def get(self, id: int) -> PhotoDocument:
        res = await self.session.execute(
            select_photo_document_by_id,
            {"id": id}
        )
        data = res.one()
        photo_document = dict_to_photo_document(data=data)
        return photo_document

    async def get_list(self) -> list[PhotoDocument]:
        results = await self.session.execute(
            select_photo_document
        )
        results = results.all()

        return [dict_to_photo_document(res) for res in results]

    async def update(self, model: PhotoDocument) -> PhotoDocument:
        search_data_dict = search_data_to_dict(model=model)
        search_data_dict["id"] = model.search_data.id
        data = photo_document_to_dict(model=model)
        data["id"] = model.id

        await self.session.execute(
            update_search_data,
            search_data_dict
        )

        await self.session.execute(
            update_photo_document,
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

