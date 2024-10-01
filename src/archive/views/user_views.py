from sqlalchemy import text
from typing import List

from src.archive.database.engine import AsyncEngine
from src.archive.gateway.converter import UserConverter
from src.archive.gateway.schemas import UserResponse, SciUserReponse
from src.archive.domains.user import Role


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


    @classmethod
    async def get_admin_users(
        cls,
        engine: AsyncEngine
    ) -> List[UserResponse]:
        async with engine.begin() as conn:
            user_row = (await conn.execute(
                text("""
                        select * from "user" where role=:role
                     """),{
                        "role": Role.AdminUser.value
                        }
                )).all()

        return UserConverter.row_to_user_list(users=user_row)


    @classmethod
    async def get_sci_users(
        cls,
        engine: AsyncEngine
    ) -> List[SciUserReponse]:
        async with engine.begin() as conn:
            user_row = (await conn.execute(
                text("""
                    select * from "user" where role=:role
                """),{
                    "role": Role.ScientificCouncil.value
                }
            )).all()
        return UserConverter.row_to_user_list(users=user_row)


    @classmethod
    async def get_redactor_users(
        cls,
        engine: AsyncEngine
    ) -> List[UserResponse]:
        async with engine.begin() as conn:
            user_row = (await conn.execute(
                text("""
                    select * from "user" where role=:role
                """), {
                    "role": Role.RedactorUser.value
                    }
            )).all()

        return UserConverter.row_to_user_list(users=user_row)


    @classmethod
    async def get_sci_group_by_coll_id(
        cls,
        coll_id: str,
        engine: AsyncEngine
    ) -> List[UserResponse]:
        async with engine.begin() as conn:
            user_row = (await conn.execute(
                text("""
                    SELECT u.*, scg.is_approved
                        FROM "user" u
                    JOIN scientific_council_group scg ON u.id = scg.scientific_council_id
                    WHERE scg.collection_id = :id
                """),{
                    "id": coll_id
                }
            )).all()

        return UserConverter.row_to_sci_user_list(users=user_row)


    @classmethod
    async def get_redactor_group_by_coll_id(
        cls,
        coll_id: str,
        engine: AsyncEngine
    ) -> List[UserResponse]:
        async with engine.begin() as conn:
            user_row = (await conn.execute(
                text("""
                    SELECT u.*
                        FROM "user" u
                    JOIN redactor_group rg ON u.id = rg.redactor_id
                    WHERE rg.collection_id = :id
                """), {
                    "id": coll_id
                }
            )).all()

        return UserConverter.row_to_user_list(users=user_row)
