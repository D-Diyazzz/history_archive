from sqlalchemy import text
from typing import List

from src.archive.database.engine import AsyncEngine
from src.archive.gateway.converter import NotificationConverter
from src.archive.gateway.schemas import NotificationAddToCollectionResponse


class NotificationViews:

    @classmethod
    async def get_notification_by_user_id(
            cls,
            id: str,
            engine: AsyncEngine
    ) -> List[NotificationAddToCollectionResponse]:
        async with engine.begin() as conn:
            notification_row = (await conn.execute(
                text("""
                     select * from notification_collection where user_id=:user_id
                """),{
                    "user_id": id
                }
            )).all()

        return NotificationConverter.row_to_notification_add_to_coll_list(notifications=notification_row)
