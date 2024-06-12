from sqlalchemy.ext.asyncio import AsyncSession

from src.archive.core import AbstractRepository
from src.archive.domains.document import PhonoDocument
from .converter import dict_to_phono_document, phono_document_to_dict
from .statements import (
    insert_phono_document,
    select_phono_document_by_id,
    select_phono_document,
    update_phono_document,
    delete_phono_document
)


class PhonoDocumentRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: PhonoDocument) -> PhonoDocument:
        phono_document_data_dict = phono_document_to_dict(model=model)

        id = await self.session.execute(
            insert_phono_document,
            phono_document_data_dict
        )

        model._id = id.scalars().first()

        return model

    async def get(self, id: int) -> PhonoDocument:
        res = await self.session.execute(
            select_phono_document_by_id,
            {"id": id}
        )
        data = res.one()
        phono_document = dict_to_phono_document(data=data)
        return phono_document

    async def get_list(self) -> list[PhonoDocument]:
        results = await self.session.execute(
            select_phono_document
        )
        results = results.all()

        return [dict_to_phono_document(res) for res in results]

    async def update(self, model: PhonoDocument) -> PhonoDocument:
        data = phono_document_to_dict(model=model)
        data["id"] = model.id

        await self.session.execute(
            update_phono_document,
            data
        )

        return model

    async def delete(self, id: int):
        await self.session.execute(
            delete_phono_document,
            {
                "id": id
            }
        )

