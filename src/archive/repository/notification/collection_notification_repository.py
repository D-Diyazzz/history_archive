from sqlalchemy.ext.asyncio import AsyncSession

from src.archive.core.repository import AbstractRepository
from src.archive.domains.notification import CollectionNotification
from .converter import collection_notification_to_dict, dict_to_collection_notification
from .statements import insert_collection_notification, delete_collection_notification, select_collection_notification_by_id, update_collection_notification


class CollectionNotificationRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: CollectionNotification):
        data = collection_notification_to_dict(model)

        id = await self.session.execute(
            insert_collection_notification,
            data
        )

        model._id = id.scalars().first()
        return model

    async def update(self, model: CollectionNotification):
        data = collection_notification_to_dict(model)

        await self.session.execute(
            update_collection_notification,
            data
        )

        return model

    async def get(self, id: int) -> CollectionNotification:
        res = await self.session.execute(
            select_collection_notification_by_id,
            {"id": id}
        )

        notification = dict_to_collection_notification(notification=res.one())

        return notification

    async def get_list(self) -> list[CollectionNotification]:
        pass

    async def delete(self, id: int):
        await self.session.execute(
            delete_collection_notification,
            {
                "id": id
            }
        )
