from datetime import datetime
from typing import List

from src.archive.core import AbstractBaseEntity
from .abstractions import SearchData, AbstarctDocument


class VideoDocument(AbstarctDocument, AbstractBaseEntity):
    def __init__(
            self,
            file_urls: List[str],
            author: str,
            dating: str,
            place_of_creating: str,
            title: str,
            volume: str,
            num_of_parts: str,
            color: str,
            creator: str,
            info_of_publication: str,
            search_data: SearchData,
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
        self._title = title
        self._volume = volume
        self._num_of_parts = num_of_parts
        self._color = color
        self._creator = creator
        self._info_of_publication = info_of_publication
        self._search_data = search_data

    @property
    def title(self) -> str:
        return self._title
    
    @property
    def volume(self) -> str:
        return self._volume
    
    @property
    def num_of_parts(self) -> str:
        return self._num_of_parts
    
    @property
    def color(self) -> str:
        return self._color
    
    @property
    def creator(self) -> str:
        return self._creator
    
    @property
    def info_of_publication(self) -> str:
        return self._info_of_publication

    @property
    def search_data(self) -> SearchData:
        return self._search_data