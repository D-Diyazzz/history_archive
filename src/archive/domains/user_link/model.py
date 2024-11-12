from uuid import UUID

from src.archive.core.base_entity import AbstractBaseEntity


class SciCouncilGroupCollectionLink(AbstractBaseEntity):

    def __init__(
        self,
        collection_id: UUID,
        scientific_council_id: UUID,
        id: int = None,
        is_approved: bool = False,
        reference = None
    ): 
        AbstractBaseEntity.__init__(self, reference)
        self._id = id
        self._collection_id = collection_id
        self._scientific_council_id = scientific_council_id
        self._is_approved = is_approved
    
    @property
    def id(self) -> int:
        return self._id

    @property
    def collection_id(self) -> UUID:
        return self._collection_id

    @property
    def scientific_council_id(self) -> UUID:
        return self._scientific_council_id

    @property
    def is_approved(self) -> bool:
        return self._is_approved

    def approve(self):
        self._is_approved = True

    def unapprove(self):
        self._is_approved = False


class RedactorGroupCollectionLink(AbstractBaseEntity):

    def __init__(
        self,
        collection_id: UUID,
        redactor_id: UUID,
        id: int = None,
        reference = None
    ):
        AbstractBaseEntity.__init__(self, reference)
        self._id = id
        self._collection_id = collection_id
        self._redactor_id = redactor_id

    @property
    def id(self) -> int:
        return self._id

    @property
    def collection_id(self) -> UUID:
        return self._collection_id

    @property
    def redactor_id(self) -> UUID:
        return self._redactor_id
