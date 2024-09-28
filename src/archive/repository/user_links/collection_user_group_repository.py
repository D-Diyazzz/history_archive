from sqlalchemy.ext.asyncio import AsyncSession

from src.archive.core.repository import AbstractLinkRepository
from src.archive.domains.user import Role
from .statements import insert_sci_council_group, delete_sci_council_group, update_sci_council_group, insert_redactor_group, delete_redactor_group, exist_redactor_in_group 


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
