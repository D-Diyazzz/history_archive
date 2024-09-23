from src.archive.core.unit_of_work import AbstractUnitOfWork
from src.archive.domains.notification import CollectionNotification


class CollectionNotificationService:

    async def read_notification(
            self,
            id: int,
            uow: AbstractUnitOfWork
    ) -> CollectionNotification:
        async with uow as uow:
            notification = await uow.repository.get(id=id)
            notification.make_it_seen()
            notification = await uow.repository.update(model=notification)
            await uow.commit()

        return notification
