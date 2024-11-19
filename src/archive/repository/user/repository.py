from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update
from sqlalchemy.exc import NoResultFound

from src.archive.core import AbstractRepository
from src.archive.domains.user import User, Role
from .converter import dict_to_user, user_to_dict
from .statements import (
    insert_user,
    select_users,
    select_user_by_id,
    update_user,
    delete_user,
    select_user_by_email
)


class UserRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: User) -> User:
        data = user_to_dict(model=model)
        res = await self.session.execute(
            insert_user,
            data
        )

        model._id = res.scalars().first()
        return model
    

    async def get(self, id: int) -> User:
        res = await self.session.execute(
            select_user_by_id,
            {"id": id}
        )

        user = dict_to_user(res.one())
        return user
    
    async def get_by_email(self, email: str) -> User:
        res = await self.session.execute(
            select_user_by_email,
            {"email": email}
        )
        res = res.one()

        if res is None:
            raise NoResultFound(f"User with this email {email} not found!")

        user = dict_to_user(res)
    
        return user
    
    async def get_list(self) -> list[User]:
        results = await self.session.execute(
            select_user
        )
        results = results.all()

        return [dict_to_user(res) for res in results]
    
    async def update(self, id: int, model: User) -> User:
        data = user_to_dict(model)

        res = await self.session.execute(
            update_user,
            data
        )

        return model
    
    async def delete(self, id: int):
        await self.session.execute(
            delete_user,
            {"id": id}
        )

