import json

from uuid import UUID, uuid4
from fastapi import Depends, UploadFile, File, Form
from fastapi.exceptions import HTTPException
from pydantic import parse_obj_as
from sqlalchemy.ext.asyncio import engine

from src.archive.core import UnitOfWork, cache_service, LinkUnitOfWork, repository
from src.archive.dependencies.auth_dependencies import check_all_admin_group_role, check_role
from src.archive.integrations.redis import RedisCacheService
from src.archive.repository.collection import CollectionRepository
from src.archive.repository.document_links import DocumentsLinkRepostiory
from src.archive.repository.notification import CollectionNotificationRepository
from src.archive.repository.user_links.sci_council_group_repository import SciCouncilGroupRepository
from src.archive.service.collection import CollectionService
from src.archive.gateway.schemas import CollectionRequest, CollectionEditRequest, CollectionPinDocumentRequest 
from src.archive.database.engine import get_session, init_engine
from src.archive.views.collection_views import CollectionViews
from src.archive.views.user_views import UserViews


service = CollectionService()
redis_service = RedisCacheService()


async def create_collection_handler(data: CollectionRequest, user_data = Depends(check_role)):

    collection = await service.create_collection(data=data,author_id=UUID(user_data["id"]), uow=UnitOfWork(reposiotry=CollectionRepository, session_factory=get_session))

    response = {
        "id": collection.id
    }
    return response


async def open_session_handler(id: str, user_data = Depends(check_role)):

    try:
        await service.connect_to_editing(user_id=user_data["id"], document_id=id, cache_service=redis_service)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


async def get_collection_admin_handler(id: str, user_data = Depends(check_all_admin_group_role)):

    response = await CollectionViews.get_collection_by_id_view(id=id, engine=init_engine())

    if redis_service.exists(id):
        user_response = await UserViews.get_user_by_id_view(id=redis_service.get(id), engine=init_engine())

        response.activeEditor = user_response

    return response


async def edit_collection_handler(id: str, data:CollectionEditRequest, user_data=Depends(check_role)):
    
    await service.edit_collection(user_id=user_data["id"], document_id=id, data=data, cache_service=redis_service, uow=UnitOfWork(reposiotry=CollectionRepository, session_factory=get_session))
    return ["200"]


async def pin_document_to_collection_handler(id: str, data:CollectionPinDocumentRequest, user_data=Depends(check_role)):
    
    id = await service.pin_document(id=id, data=data, uow=LinkUnitOfWork(reposiotry=DocumentsLinkRepostiory, session_factory=get_session))
    return {"link_id": id}


async def delete_document_link_handler(id: str, data: CollectionPinDocumentRequest, user_data=Depends(check_role)):

    await service.delete_document_link(id=id, data=data, uow=LinkUnitOfWork(reposiotry=DocumentsLinkRepostiory, session_factory=get_session))
    return ["200"]


async def bind_user_to_collection_handler(id: str, user_id: str, user_data=Depends(check_role)):

    user = await UserViews.get_user_by_id_view(id=user_id, engine=init_engine())

    await service.bind_user_to_scientific_group(coll_id=id, user_data=user,uow=UnitOfWork(reposiotry=CollectionNotificationRepository, link_repository=SciCouncilGroupRepository, session_factory=get_session))
    return ["200"]
