from fastapi import Depends, HTTPException

from src.archive.core import UnitOfWork2
from src.archive.dependencies.auth_dependencies import check_role, check_super_admin_role
from src.archive.gateway.schemas import UserChangeRoleRequest
from src.archive.repository import RepositoryFactory
from src.archive.service.user import UserService
from src.archive.views import UserViews
from src.archive.database.engine import get_session, init_engine


service = UserService()
uow2 = UnitOfWork2(session_factory=get_session, repository_factory=RepositoryFactory)

async def get_admin_users_handler(user_data = Depends(check_role)):
    users = await UserViews.get_admin_users(engine=init_engine())
    return users


async def get_sci_users_handler(user_data=Depends(check_role)):
    users = await UserViews.get_sci_users(engine=init_engine())
    return users


async def get_redactor_users_handler(user_data=Depends(check_role)):
    users = await UserViews.get_redactor_users(engine=init_engine())
    return users


async def change_user_role_handler(id: str, data: UserChangeRoleRequest, user_data=Depends(check_super_admin_role)):
    try:
        await service.change_user_role(id=id, data=data, uow=uow2)
    except ValueError as e:
        return HTTPException(status_code=400, detail=str(e))
    return ["200"]
