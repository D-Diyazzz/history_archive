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