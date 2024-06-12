from sqlalchemy.ext.asyncio import AsyncSession

from src.archive.core import AbstractRepository
from src.archive.domains.document import VideoDocument
from .converter import dict_to_video_document, video_document_to_dict, search_data_to_dict
from .statements import (
    insert_video_document,
    insert_search_data,
    select_video_document_by_id,
    select_video_document,
    update_video_document,
    update_search_data,
    delete_search_data
)


class VideoDocumentRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: VideoDocument) -> VideoDocument:
        search_data_dict = search_data_to_dict(model=model)

        search_data_id = await self.session.execute(
            insert_search_data,
            search_data_dict
        )

        search_data_id = search_data_id.scalars().first()
        model._search_data._id = search_data_id
        video_document_data_dict = video_document_to_dict(model=model)

        id = await self.session.execute(
            insert_video_document,
            video_document_data_dict
        )

        model._id = id.scalars().first()

        return model

    async def get(self, id: int) -> VideoDocument:
        res = await self.session.execute(
            select_video_document_by_id,
            {"id": id}
        )
        data = res.one()
        video_document = dict_to_video_document(data=data)
        return video_document

    async def get_list(self) -> list[VideoDocument]:
        results = await self.session.execute(
            select_video_document
        )
        results = results.all()

        return [dict_to_video_document(res) for res in results]

    async def update(self, model: VideoDocument) -> VideoDocument:
        search_data_dict = search_data_to_dict(model=model)
        search_data_dict["id"] = model.search_data.id
        data = video_document_to_dict(model=model)
        data["id"] = model.id

        await self.session.execute(
            update_search_data,
            search_data_dict
        )

        await self.session.execute(
            update_video_document,
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

