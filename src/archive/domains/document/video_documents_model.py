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

    def update(
            self,
            new_file_urls: List[str] = None,
            new_author: str = None,
            new_dating: str = None,
            new_place_of_creating: str = None,
            new_title: str = None,
            new_volume: str = None,
            new_num_of_parts: str = None,
            new_color: str = None,
            new_creator: str = None,
            new_info_of_publication: str = None,
            updated_search_data: SearchData = None
    ):
        self._file_urls = new_file_urls if new_file_urls else self._file_urls
        self._author = new_author if new_author else self._author
        self._dating = new_dating if new_dating else self._dating
        self._place_of_creating = new_place_of_creating if new_place_of_creating else self._place_of_creating
        self._title = new_title if new_title else self._title
        self._volume = new_volume if new_volume else self._volume
        self._num_of_parts = new_num_of_parts if new_num_of_parts else self._num_of_parts
        self._color = new_color if new_color else self._color
        self._creator = new_creator if new_creator else self._creator
        self._info_of_publication = new_info_of_publication if new_info_of_publication else self._info_of_publication
        self._search_data = updated_search_data if updated_search_data else self._search_data

