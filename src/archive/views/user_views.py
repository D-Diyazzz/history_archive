from sqlalchemy import text

from src.archive.database.engine import AsyncEngine
from src.archive.gateway.converter import UserConverter
from src.archive.gateway.schemas import UserResponse


class UserViews:

    @classmethod
    async def get_user_by_id_view(
        cls,
        id: str,
        engine: AsyncEngine
    ) -> UserResponse:
        async with engine.begin() as conn:
            user_row = (await conn.execute(
                text("""
                    select * from "user" where id=:id
                """),{
                    "id": id
                }
            )).one()

        return UserConverter.row_to_user(user=user_row)
