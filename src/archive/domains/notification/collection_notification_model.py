from datetime import datetime

from src.archive.core.base_entity import AbstractBaseEntity


class CollectionNotification(AbstractBaseEntity):
    def __init__(
        self,
        collection_id: str,
        user_id : str,
        id: int = None,
        is_seen: bool = False,
        created_at: datetime = None,
        reference = None
    ):
        AbstractBaseEntity.__init__(self, reference)
        self._id = id
        self._user_id = user_id
        self._collection_id = collection_id
        self._is_seen = is_seen
        self._created_at = created_at or datetime.utcnow()
    
    @property
    def id(self) -> int:
        return self._id

    @property
    def collection_id(self) -> str:
        return self._collection_id

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def is_seen(self) -> bool:
        return self._is_seen

    @property
    def created_at(self) -> datetime:
        return self._created_at

    def make_it_seen(self):
        self._is_seen = True

