from fastapi import Depends

from src.archive.core import repository
from src.archive.core.unit_of_work import UnitOfWork
from src.archive.database.engine import get_session, init_engine
from src.archive.dependencies.auth_dependencies import check_role
from src.archive.gateway.converter.notification_converter import NotificationConverter
from src.archive.repository.notification.collection_notification_repository import CollectionNotificationRepository
from src.archive.service.notification.collection_notification_service import CollectionNotificationService
from src.archive.views import NotificationViews


service = CollectionNotificationService()

async def get_notifications_handler(id: str, user_data=Depends(check_role)):
    notifications = await NotificationViews.get_notification_by_user_id(id=id, engine=init_engine())
    
    return notifications


async def read_collection_notification_handler(id: int, user_data=Depends(check_role)):
    notification = await service.read_notification(id=id, uow=UnitOfWork(reposiotry=CollectionNotificationRepository, session_factory=get_session))
    
    return ["200"] 
