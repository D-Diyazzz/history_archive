from datetime import datetime
from typing import List

from src.archive.core import AbstractBaseEntity
from .abstractions import AbstarctDocument


class PhonoDocument(AbstarctDocument, AbstractBaseEntity):
    def __init__(
            self,
            file_urls: List[str],
            author: str,
            dating: str,
            place_of_creating: str,
            genre: str,
            brief_summary: str,
            addressee: str,
            cypher: str,
            lang: str,
            storage_media: str,
            id: int = None,
            created_at: datetime = None,
            reference = None
    ):
        AbstarctDocument.__init__(
            self=self,
            file_urls=file_urls, 
            author=author, 
            dating=dating, 
            place_of_creating=place_of_creating, 
            id=id, 
            created_at=created_at
        )
        AbstractBaseEntity.__init__(self, reference)
        self._genre = genre
        self._brief_summary = brief_summary
        self._addressee = addressee
        self._cypher = cypher
        self._lang = lang
        self._storage_media = storage_media
       

    @property
    def genre(self) -> str:
        return self._genre
    
    @property
    def brief_summary(self) -> str:
        return self._brief_summary
    
    @property
    def addressee(self) -> str:
        return self._addressee
    
    @property
    def cypher(self) -> str:
        return self._cypher
    
    @property
    def lang(self) -> str:
        return self._lang
    
    @property
    def storage_media(self) -> str:
        return self._storage_media