import pytz

from dataclasses import dataclass
from datetime import datetime

from src.archive.core import AbstractBaseEntity

@dataclass(frozen=True)
class Type:
    id: int
    name: str | None

@dataclass(frozen=True)
class Class:
    id: int
    name: str | None

@dataclass(frozen=True)
class Format:
    id: int
    name: str | None

@dataclass(frozen=True)
class Method:
    id: int
    name: str | None

class Collection(AbstractBaseEntity):

    def __init__(
            self, 
            file_url: str,
            theme: str,
            purpose: str,
            task: str,
            type_coll: Type,
            class_coll: Class,
            format_coll: Format,
            method_coll: Method,
            id=None,
            preface: str = None,
            note: str = None,
            indication: str = None,
            intro_text: str = None,
            recommendations: str = None,
            created_at: datetime = None,
            reference=None):
        self._id = id
        self._file_Url = file_url
        self._theme = theme
        self._purpose = purpose
        self._task = task
        self._type_coll = type_coll
        self._class_coll = class_coll
        self._format_coll = format_coll
        self._method_coll = method_coll
        self._preface = preface
        self._note = note
        self._indication = indication
        self._intro_text = intro_text
        self._recommendations = recommendations
        self._created_at = created_at if created_at else datetime.now(pytz.UTC)
        super().__init__(reference)

    @property
    def get_id(self) -> int:
        return self._id
    
    @property
    def get_file_url(self) -> str:
        return self._file_Url
    
    @property
    def get_theme(self) -> str:
        return self._theme
    
    @property
    def get_purpose(self) -> str:
        return self._purpose
    
    @property
    def get_task(self) -> str:
        return self._task
    
    @property
    def get_type_coll(self) -> Type:
        return self._type_coll
    
    @property
    def get_class_coll(self) -> Class:
        return self._class_coll
    
    @property
    def get_format_coll(self) -> Format:
        return self._format_coll
    
    @property
    def get_method_coll(self) -> Method:
        return self._method_coll
    
    @property
    def get_preface(self) -> str:
        return self._preface
    
    @property
    def get_note(self) -> str:
        return self._note
    
    @property
    def get_indication(self) -> str:
        return self._indication
    
    @property
    def get_intro_text(self) -> str:
        return self._intro_text
    
    @property
    def get_recommendations(self) -> str:
        return self._recommendations

    @property
    def get_created_at(self) -> datetime:
        return self._created_at
    
    def update_fields(
            self, 
            file_url: str = None,
            theme: str = None,
            purpose: str = None,
            task: str = None,
            type_coll: Type = None,
            class_coll: Class = None,
            format_coll: Format = None,
            method_coll: Method = None,
            preface: str = None,
            note: str = None,
            indication: str = None,
            intro_text: str = None,
            recommendations: str = None,
    ):
        pass  