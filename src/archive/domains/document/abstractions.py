import pytz
from datetime import datetime
from abc import ABC        


class AbstarctDocument(ABC):
    def __init__(
            self,
            file_url: str,
            author: str,
            dating: str,
            place_of_creating: str,
            id: int = None,
            created_at: datetime = None
    ):
        self._id = id
        self._file_url = file_url
        self._author = author
        self._dating = dating
        self._place_of_creating = place_of_creating
        self._created_at = created_at if created_at else datetime.now(pytz.UTC)

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def file_url(self) -> str:
        return self._file_url
    
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