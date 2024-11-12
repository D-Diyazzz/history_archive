import pytz
from datetime import datetime
from uuid import UUID

from src.archive.core import AbstractBaseEntity


class CollectionComment(AbstractBaseEntity):
    def __init__(
        self,
        collection_id: UUID,
        user_id: UUID,
        text: str,
        id: int = None,
        created_at: datetime = None,
        reference = None
    ):
        AbstractBaseEntity.__init__(self, reference)
        self._id = id
        self._collection_id = collection_id
        self._user_id = user_id
        self._text = text
        self._created_at = created_at or datetime.utcnow(pytz.UTC)

    @property
    def id(self) -> int:
        return self._id

    @property
    def collection_id(self) -> UUID:
        return self._collection_id

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def text(self) -> str:
        return self._text

    @property
    def created_at(self) -> datetime:
        return self._created_at

    def update_text(self, new_text):
        self._text = new_text
