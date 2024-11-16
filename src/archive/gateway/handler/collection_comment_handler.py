from fastapi import Depends

from src.archive.core import UnitOfWork2
from src.archive.database.engine import get_session, init_engine
from src.archive.dependencies.auth_dependencies import check_all_admin_group_role
from src.archive.repository import RepositoryFactory
from src.archive.service.collection_comment import CollectionCommentService
from src.archive.views.collection_views import CollectionViews
from src.archive.gateway.schemas import CollectionCommentEditRequest


service = CollectionCommentService()
uow2 = UnitOfWork2(session_factory=get_session, repository_factory=RepositoryFactory)


async def get_user_collection_comment_handler(id: str, user_data=Depends(check_all_admin_group_role)):
    
    comment = await CollectionViews.get_user_comment(coll_id=id, user_id=user_data["id"], engine=init_engine())
    return comment

async def edit_collection_comment_handler(id: str, data: CollectionCommentEditRequest, user_data=Depends(check_all_admin_group_role)):
    
    await service.edit_comment(
        coll_id=id,
        user_id=user_data["id"],
        comment_id=data.id,
        text=data.text,
        uow=uow2
    )
    return 200


async def get_user_collection_comment_by_user_id_handler(id: str, user_id:str, user_data=Depends(check_all_admin_group_role)):

    comment = await CollectionViews.get_user_comment(coll_id=id, user_id=user_id, engine=init_engine())
    return comment
