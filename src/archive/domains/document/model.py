import pytz

from datetime import datetime

from src.archive.core import AbstractBaseEntity


class Document(AbstractBaseEntity):

    def __init__(
            self,
            file_url: str,
            title: str,
            heading: str,
            author: str,
            description_content: str,
            dating: str,
            legends: str,
            format_doc: str,
            color_palette: str,
            resolution: str,
            compression: str,
            scanner_model: str,
            created_at: datetime = None,
            id: int = None,
            reference = None
    ):
        self._id = id
        self._file_url = file_url
        self._title = title
        self._heading = heading
        self._author = author
        self._description_content = description_content
        self._dating = dating
        self._legends = legends
        self._format_doc = format_doc
        self._color_palette = color_palette
        self._resolution = resolution
        self._compression = compression
        self._scanner_model = scanner_model
        self._created_at = created_at if created_at else datetime.now(pytz.UTC)
        super().__init__(reference)

    
    @property
    def get_id(self) -> int:
        return self._id
    
    @property
    def get_file_url(self) -> str:
        return self._file_url
    
    @property
    def get_title(self) -> str:
        return self._title
    
    @property
    def get_heading(self) -> str:
        return self._heading
    
    @property
    def get_author(self) -> str:
        return self._author
    
    @property
    def get_description_content(self) -> str:
        return self._description_content
    
    @property
    def get_dating(self) -> str:
        return self._dating
    
    @property
    def get_legends(self) -> str:
        return self._legends
    
    @property
    def get_format_doc(self) -> str:
        return self._format_doc
    
    @property
    def get_color_palette(self) -> str:
        return self._color_palette
    
    @property
    def get_resolution(self) -> str:
        return self._resolution
    
    @property
    def get_compression(self) -> str:
        return self._compression
    
    @property
    def get_scanner_model(self) -> str:
        return self._scanner_model
    
    @property
    def get_created_at(self) -> datetime:
        return self._created_at