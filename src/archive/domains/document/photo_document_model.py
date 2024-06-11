from datetime import datetime
from typing import List

from src.archive.core import AbstractBaseEntity
from .abstractions import SearchData, AbstarctDocument


class PhotoDocument(AbstarctDocument, AbstractBaseEntity):
    def __init__(
            self,
            file_urls: List[str],
            author: str,
            dating: str,
            place_of_creating: str,
            title: str,
            completeness_of_reproduction: str,
            storage_media: str,
            color: str,
            size_of_original: str,
            image_scale: str,
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
        self._completeness_of_reproduction = completeness_of_reproduction
        self._storage_media = storage_media
        self._color = color
        self._size_of_original = size_of_original
        self._image_scale = image_scale
        self._search_data = search_data

    @property
    def title(self) -> str:
        return self._title
    
    @property
    def completeness_of_reproduction(self) -> str:
        return self._completeness_of_reproduction
    
    @property
    def storage_media(self) -> str:
        return self._storage_media
    
    @property
    def color(self) -> str:
        return self._color
    
    @property
    def size_of_original(self) -> str:
        return self._size_of_original
    
    @property
    def image_scale(self) -> str:
        return self._image_scale

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
            new_completeness_of_reproduction: str = None,
            new_storage_media: str = None,
            new_color: str = None,
            new_size_of_original: str = None,
            new_image_scale: str = None,
            updated_search_data: SearchData = None
    ):
        self._file_urls = new_file_urls if new_file_urls else self._file_urls
        self._author = new_author if new_author else self._author
        self._dating = new_dating if new_dating else self._dating
        self._place_of_creating = new_place_of_creating if new_place_of_creating else self._place_of_creating
        self._title = new_title if new_title else self._title
        self._completeness_of_reproduction = new_completeness_of_reproduction if new_completeness_of_reproduction else self._completeness_of_reproduction
        self._storage_media = new_storage_media if new_storage_media else self._storage_media
        self._color = new_color if new_color else self._color
        self._size_of_original = new_size_of_original if new_size_of_original else self._size_of_original
        self._image_scale = new_image_scale if new_image_scale else self._image_scale
        self._search_data = updated_search_data if updated_search_data else self._search_data

