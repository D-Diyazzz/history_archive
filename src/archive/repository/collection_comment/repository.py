from sqlalchemy.ext.asyncio import AsyncSession

from src.archive.core import AbstractRepository
from src.archive.domains.collection_comment import CollectionComment
from .converter import collection_comment_to_dict, dict_to_collection_comment
from .statements import insert_collection_comment, select_collection_comment, select_collection_comment_by_id, update_collection_comment, delete_collection_comment


class CollectionCommentRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: CollectionComment) -> CollectionComment:
        data = collection_comment_to_dict(model)

        id = await self.session.execute(
            insert_collection_comment,
            data
        )

        model._id = id.scalars().first()
        return model

    async def get(self, id: int) -> CollectionComment:
        res = await self.session.execute(
            select_collection_comment_by_id,
            {"id": id}
        )

        coll_comment = dict_to_collection_comment(res.one())
        return coll_comment

    async def get_list(self) -> list[CollectionComment]:
        res = await self.session.execute(
            select_collection_comment,
        )
        res = res.all()

        return [dict_to_collection_comment(r) for r in res]

    async def update(self, model: CollectionComment):
        data = collection_comment_to_dict(model)

        await self.session.execute(
            update_collection_comment,
            data
        )

        return model

    async def delete(self, id: int):
        await self.session.execute(
            delete_collection_comment,
            {
                "id": id
            }
        )
