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

    def update(
            self,
            new_file_urls: List[str] = None,
            new_author: str = None,
            new_dating: str = None,
            new_place_of_creating: str = None,
            new_genre: str = None,
            new_brief_summary: str = None,
            new_addressee: str = None,
            new_cypher: str = None,
            new_lang: str = None,
            new_storage_media: str = None
    ):
        self._file_urls = new_file_urls if new_file_urls else self._file_urls
        self._author = new_author if new_author else self._author
        self._dating = new_dating if new_dating else self._dating
        self._place_of_creating = new_place_of_creating if new_place_of_creating else self._place_of_creating
        self._genre = new_genre if new_genre else self._genre
        self._brief_summary = new_brief_summary if new_brief_summary else self._brief_summary
        self._addressee = new_addressee if new_addressee else self._addressee
        self._cypher = new_cypher if new_cypher else self._cypher
        self._lang = new_lang if new_lang else self._lang
        self._storage_media = new_storage_media if new_storage_media else self._storage_media

    def remove_url_files_from_files(
            self,
            file_urls: List[str]
    ):
        for file in file_urls:
            self._file_urls = [f for f in self._file_urls if f != file]
