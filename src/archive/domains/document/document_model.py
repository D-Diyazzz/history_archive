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
    
    def update(
            self,
            new_file_url: str = None,
            new_author: str = None,
            new_dating: str = None,
            new_place_of_creating: str = None,
            new_variety: str = None,
            new_addressee: str = None,
            new_brief_content: str = None,
            new_case_prod_number: str = None,
            new_main_text: str = None,
            updated_search_data: SearchData = None,
    ):
        self._file_url = new_file_url if new_file_url else self._file_url
        self._author = new_author if new_author else self._author
        self._dating = new_dating if new_dating else self._dating
        self._place_of_creating = new_place_of_creating if new_place_of_creating else self._place_of_creating
        self._variety = new_variety if new_variety else self._variety
        self._addressee = new_addressee if new_addressee else self._addressee
        self._brief_content = new_brief_content if new_brief_content else self._brief_content
        self._case_prod_number = new_case_prod_number if new_case_prod_number else self._case_prod_number
        self._main_text = new_main_text if new_main_text else self._main_text
        self._search_data = updated_search_data if updated_search_data else self._search_data
