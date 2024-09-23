from sqlalchemy import Row
from typing import List

from src.archive.gateway.schemas import NotificationAddToCollectionResponse


class NotificationConverter:

    @classmethod
    def row_to_notification_add_to_coll(cls, notification: Row) -> NotificationAddToCollectionResponse:
        return NotificationAddToCollectionResponse(
            id=notification.id,
            coll_id=str(notification.collection_id),
            user_id=str(notification.user_id),
            is_seen=notification.is_seen,
            created_at=notification.created_at
        )

    @classmethod
    def row_to_notification_add_to_coll_list(cls, notifications: Row) -> List[NotificationAddToCollectionResponse]:
        return [cls.row_to_notification_add_to_coll(notification) for notification in notifications]
