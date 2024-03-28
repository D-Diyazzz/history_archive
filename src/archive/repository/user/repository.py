from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update

from src.archive.core import AbstractRepository
from src.archive.domains.user import User, Role
from .converter import dict_to_user, user_to_dict


class UserRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: User) -> User:
        data = user_to_dict(model=model)
        res = await self.session.execute(insert(User), data)
    

    async def get(self, id: int) -> User:
        res = await self.session.execute(select(User).filter_by(id=id))

        user = dict_to_user(res.scalars().first())
        return user
    
    async def get_by_email(self, email: str) -> User:
        res = await self.session.execute(select(User).filter_by(email=email))

        user = dict_to_user(res.scalars().first())
        return user
    
    async def get_list(self) -> list[User]:
        results = await self.session.execute(select(User))
        results = results.scalars().all()

        return [dict_to_user(res) for res in results]
    
    async def update(self, id: int, data: User) -> User:
        data = user_to_dict(data)

        res = await self.session.execute(update(User).filter_by(id=id).returning(User), data)

        user = dict_to_user(res.scalars().first())
        return user
    
    async def delete(self, id: int):
        await self.session.execute(delete(User).filter_by(id=id))

