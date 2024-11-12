from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.archive.core.repository import AbstractLinkRepository, AbstractRepository
from src.archive.domains.user import Role
from src.archive.domains.user_link import SciCouncilGroupCollectionLink, RedactorGroupCollectionLink 
from .statements import (
    insert_sci_council_group, 
    delete_sci_council_group, 
    update_sci_council_group, 
    insert_redactor_group, 
    delete_redactor_group, 
    exist_redactor_in_group, 
    select_sci_council_group_by_id, 
    select_redactor_group_by_id, 
    select_sci_council_group, 
    select_redactor_group, 
    select_sci_council_group_by_coll_and_user_id, 
    select_redactor_group_by_coll_and_user_id,
    delete_sci_council_group_by_coll_and_user_id,
    delete_redactor_group_by_coll_and_user_id,
)


class SciCouncilGroupCollectionLinkRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: SciCouncilGroupCollectionLink) -> SciCouncilGroupCollectionLink:
    
        result = await self.session.execute(
            insert_sci_council_group,
            {
                "collection_id": model.collection_id,
                "sci_council_id": model.scientific_council_id,
                "is_approved": model.is_approved
            }
        )

        # Обновляем ID в модели
        model._id = result.scalars().first()
        return model

    async def get(self, id: int) -> SciCouncilGroupCollectionLink:
        # Получаем запись по ID
        result = await self.session.execute(
            select_sci_council_group_by_id,
            {"id": id}
        )

        # Конвертируем запись в объект модели
        data = result.one()
        sci_council_link = SciCouncilGroupCollectionLink(
            id=data["id"],
            collection_id=UUID(data["collection_id"]),
            scientific_council_id=UUID(data["scientific_council_id"]),
            is_approved=data["is_approved"],
        )
        return sci_council_link

    async def get_by_coll_and_user_id(self, coll_id: UUID, user_id: UUID):
        result = await self.session.execute(
            select_sci_council_group_by_coll_and_user_id,
            {
                "collection_id": coll_id,
                "sci_council_id": user_id
            }
        )
        data = result.one()
        print(data.id)
        sci_council_link = SciCouncilGroupCollectionLink(
            id=int(data.id),
            collection_id=UUID(data.collection_id),
            scientific_council_id=UUID(data.scientific_council_id),
            is_approved=data.is_approved,
        )
        return sci_council_link

    async def get_list(self) -> list[SciCouncilGroupCollectionLink]:
        # Получаем все записи
        result = await self.session.execute(
            select_sci_council_group
        )
        
        # Преобразуем записи в объекты модели
        records = result.all()
        return [dict_to_sci_council_group_collection_link(record) for record in records]

    async def update(self, model: SciCouncilGroupCollectionLink):
               # Обновляем запись
        await self.session.execute(
            update_sci_council_group,
            {
                "is_approved": model.is_approved,
                "collection_id": model.collection_id,
                "scientific_council_id": model.scientific_council_id
            }
        )

        return model

    async def delete(self, id: int):
        # Удаляем запись по ID
        await self.session.execute(
            delete_sci_council_group,
            {
                "id": id
            }
        )

    async def delete_by_coll_and_user_id(self, coll_id: UUID, user_id:UUID):
        await self.session.execute(
            delete_sci_council_group_by_coll_and_user_id,
            {
                "collection_id": coll_id,
                "sci_council_id": user_id
            }
        )        



class RedactorGroupCollectionLinkRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: RedactorGroupCollectionLink) -> SciCouncilGroupCollectionLink:
    
        result = await self.session.execute(
            insert_redactor_group,
            {
                "collection_id": model.collection_id,
                "redactor_id": model.redactor_id,
            }
        )

        # Обновляем ID в модели
        model._id = result.scalars().first()
        return model

    async def get(self, id: int) -> SciCouncilGroupCollectionLink:
        # Получаем запись по ID
        result = await self.session.execute(
            select_redactor_group_by_id,
            {"id": id}
        )

        # Конвертируем запись в объект модели
        data = result.one()
        redactor_link = RedactorGroupCollectionLink(
            id=data["id"],
            collection_id=UUID(data["collection_id"]),
            redactor_id=UUID(data["scientific_council_id"]),
        )
        return redactor_link

    async def get_list(self) -> list[SciCouncilGroupCollectionLink]:
        # Получаем все записи
        result = await self.session.execute(
            select_redactor_group
        )
        
        # Преобразуем записи в объекты модели
        records = result.all()
        return [dict_to_sci_council_group_collection_link(record) for record in records]

    async def get_by_coll_and_user_id(self, coll_id: UUID, user_id: UUID):
        
        result = await self.session.execute(
            select_redactor_group_by_coll_and_user_id,
            {
                "collection_id": coll_id,
                "redactor_id": user_id
            }
        )
        data = result.one()
        redactor_link = RedactorGroupCollectionLink(
            id=data["id"],
            collection_id=UUID(data["collection_id"]),
            redactor_id=UUID(data["scientific_council_id"]),
        )
        return redactor_link


    async def update(self, model: SciCouncilGroupCollectionLink):
        pass

    async def delete(self, id: int):
        # Удаляем запись по ID
        await self.session.execute(
            delete_redactor_group,
            {
                "id": id
            }
        )
    async def delete_by_coll_and_user_id(self, coll_id: UUID, user_id:UUID):
        await self.session.execute(
            delete_redactor_group_by_coll_and_user_id,
            {
                "collection_id": coll_id,
                "redactor_id": user_id
            }
        )

class CollectionUserGroupRepository(AbstractLinkRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, obj_id: str, related_obj_id: str, **kwargs) -> int:
        if kwargs["user_role"] == Role.ScientificCouncil.value:
            id = await self.session.execute(
                insert_sci_council_group,
                {
                    "collection_id": obj_id,
                    "sci_council_id": related_obj_id,
                    "is_approved": False
                }
            )
            return id.scalar()
        elif kwargs["user_role"] == Role.RedactorUser.value:
            id = await self.session.execute(
                insert_redactor_group,
                {
                    "collection_id": obj_id,
                    "redactor_id": related_obj_id
                }
            )
            return id.scalar()
        else:
            raise ValueError("")

    async def update(self, obj_id: str, related_obj_id: str, **kwargs):
        if kwargs["user_role"] == Role.ScientificCouncil.value:
            await self.session.execute(
                update_sci_council_group,
                {
                    "collection_id": obj_id,
                    "sci_council_id": related_obj_id,
                    "is_approved": kwargs["approve"]
                }
            )
        else:
            raise ValueError("")

    async def exist(self, obj_id: str, related_obj_id: str, **kwargs):
        if kwargs["user_role"] == Role.ScientificCouncil.value:
            pass
        elif kwargs["user_role"] == Role.RedactorUser.value:
            res = await self.session.execute(
                exist_redactor_in_group,
                {
                    "collection_id": obj_id,
                    "redactor_id": related_obj_id
                }
            )
            return res.scalar()


    async def delete(self, obj_id: str, related_obj_id: str, **kwargs):
        if kwargs["user_role"] == Role.ScientificCouncil.value:
            await self.session.execute(
                delete_sci_council_group,
                {
                    "collection_id": obj_id,
                    "sci_council_id": related_obj_id
                }
            )
        elif kwargs["user_role"] == Role.RedactorUser.value:
            await self.session.execute(
                delete_redactor_group,
                {
                    "collection_id": obj_id,
                    "redactor_id": related_obj_id
                }
            )
        else:
            raise ValueError("")
