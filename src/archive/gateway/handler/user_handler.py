from fastapi import Depends

from src.archive.dependencies.auth_dependencies import check_role
from src.archive.views import UserViews
from src.archive.database.engine import get_session, init_engine


async def get_admin_users_handler(user_data = Depends(check_role)):
    users = await UserViews.get_admin_users(engine=init_engine())
    return users
