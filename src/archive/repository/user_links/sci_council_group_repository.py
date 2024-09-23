from sqlalchemy.ext.asyncio import AsyncSession

from src.archive.core.repository import AbstractLinkRepository
from .statements import insert_sci_council_group, delete_sci_council_group 


class SciCouncilGroupRepository(AbstractLinkRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, obj_id: str, related_obj_id: str, **kwargs) -> int:
        id = await self.session.execute(
            insert_sci_council_group,
            {
                "collection_id": obj_id,
                "sci_council_id": related_obj_id,
                "is_approved": False
            }
        )
        return id.scalar()


    async def delete(self, obj_id: str, related_obj_id: str, **kwargs):
        await self.session.execute(
            delete_sci_council_group,
            {
                "collection_id": obj_id,
                "sci_council_id": related_obj_id
            }
        )
