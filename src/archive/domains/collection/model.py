import hashlib
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from src.archive.core import AbstractBaseEntity


class Collection(AbstractBaseEntity):
    def __init__(
            self,
            file_url: str,
            html_url: str,
            theme: str,
            title: str,
            author_id: UUID,
            id: UUID = None,
            is_approved: bool = False,
            created_at: datetime = None,
            hash_code: str = None,
            reference = None
    ):
        AbstractBaseEntity.__init__(self, reference)
        self._id = id or uuid4()
        self._file_url = file_url
        self._html_url = html_url
        self._theme = theme
        self._title = title
        self._author_id = author_id
        self._is_approved = is_approved
        self._created_at = created_at or datetime.utcnow()
        self._hash_code = hash_code or self.generate_hash_code()

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def file_url(self) -> str:
        return self._file_url

    @property
    def html_url(self) -> str:
        return self._html_url

    @property
    def theme(self) -> str:
        return self._theme

    @property
    def title(self) -> str:
        return self._title

    @property
    def author_id(self) -> UUID:
        return self._author_id

    @property
    def is_approved(self) -> bool:
        return self._is_approved

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def hash_code(self) -> str:
        return self._hash_code

    def generate_hash_code(self) -> str:
        hash_input = f"{self._file_url}{self._html_url}".encode('utf-8')
        full_hash = hashlib.sha256(hash_input).hexdigest()
        return full_hash[:7]  

    def update(
            self,
            new_theme: Optional[str] = None,
            new_title: Optional[str] = None,
    ):
        if new_theme:
            self._theme = new_theme
        if new_title:
            self._title = new_title

    def to_approve(self):
        self._is_approved = True

    def dont_approve(self):
        self._is_approved = False
