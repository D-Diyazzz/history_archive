from datetime import datetime

from src.archive.core import AbstractBaseEntity
from .abstractions import SearchData, AbstarctDocument


class Document(AbstarctDocument, AbstractBaseEntity):
    def __init__(
            self,
            file_url: str,
            author: str,
            dating: str,
            place_of_creating: str,
            variety: str,
            addressee: str,
            brief_content: str,
            case_prod_number: str,
            main_text: str,
            search_data: SearchData,
            id: int = None,
            created_at: datetime = None,
            reference = None
    ):
        AbstarctDocument.__init__(
            self=self,
            file_url=file_url, 
            author=author, 
            dating=dating, 
            place_of_creating=place_of_creating, 
            id=id, 
            created_at=created_at
        )
        AbstractBaseEntity.__init__(self, reference)
        self._variety = variety
        self._addressee = addressee
        self._brief_content = brief_content
        self._case_prod_number = case_prod_number
        self._main_text = main_text
        self._search_data = search_data

    @property
    def variety(self) -> str:
        return self._variety
    
    @property
    def addressee(self) -> str:
        return self._addressee
    
    @property
    def brief_content(self) -> str:
        return self._brief_content
    
    @property
    def case_prod_number(self) -> str:
        return self._case_prod_number
    
    @property
    def main_text(self) -> str:
        return self._main_text

    @property
    def search_data(self) -> SearchData:
        return self._search_data