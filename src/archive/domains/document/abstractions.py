import pytz
from uuid import UUID, uuid4
from datetime import datetime
from abc import ABC        
from typing import List


class AbstarctDocument(ABC):
    def __init__(
            self,
            file_urls: List[str],
            author: str,
            dating: str,
            place_of_creating: str,
            id: int = None,
            created_at: datetime = None
    ):
        self._id = id or uuid4()
        self._file_urls = file_urls
        self._author = author
        self._dating = dating
        self._place_of_creating = place_of_creating
        self._created_at = created_at if created_at else datetime.now(pytz.UTC)

    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def file_urls(self) -> List[str]:
        return self._file_urls
    
    @property
    def author(self) -> str:
        return self._author
    
    @property
    def dating(self) -> str:
        return self._dating
    
    @property
    def place_of_creating(self) -> str:
        return self._place_of_creating
    
    @property
    def created_at(self) -> dating:
        return self._created_at

    def remove_url_files_from_files(self, file_urls: List[str]):
        return NotImplementedError
    

class SearchData:
    def __init__(
            self,
            cypher: str,
            fund: str,
            inventory: str,
            case: str,
            leaf: str,
            authenticity: str,
            lang: str,
            playback_method: str,
            other: str = None,
            id: int = None
    ):
        self._id = id
        self._cypher = cypher
        self._fund = fund
        self._inventory = inventory
        self._case = case
        self._leaf = leaf
        self._authenticity = authenticity
        self._lang = lang
        self._playback_method = playback_method
        self._other = other


    def update(
        self,
        new_cypher: str = None,
        new_fund: str = None,
        new_inventory: str = None,
        new_case: str = None,
        new_leaf: str = None,
        new_authenticity: str = None,
        new_lang: str = None,
        new_playback_method: str = None,
        new_other: str = None
    ):
        self._cypher = new_cypher if new_cypher else self._cypher
        self._fund = new_fund if new_fund else self._fund
        self._inventory = new_inventory if new_inventory else self._inventory
        self._case = new_case if new_case else self._case
        self._leaf = new_leaf if new_leaf else self._leaf
        self._authenticity = new_authenticity if new_authenticity else self._authenticity
        self._lang = new_lang if new_lang else self._lang
        self._playback_method = new_playback_method if new_playback_method else self._playback_method
        self._other = new_other if new_other else self._other


    @property
    def id(self) -> int:
        return self._id

    @property
    def cypher(self) -> str:
        return self._cypher

    @property
    def fund(self) -> str:
        return self._fund

    @property
    def inventory(self) -> str:
        return self._inventory

    @property
    def case(self) -> str:
        return self._case

    @property
    def leaf(self) -> str:
        return self._leaf

    @property
    def authenticity(self) -> str:
        return self._authenticity

    @property
    def lang(self) -> str:
        return self._lang

    @property
    def playback_method(self) -> str:
        return self._playback_method

    @property
    def other(self) -> str:
        return self._other
