from pydantic import BaseModel
from datetime import datetime


class DocumentRequest(BaseModel):
    file_url: str
    title: str
    heading: str
    author: str
    description_content: str
    dating: str
    legends: str
    format_doc: str
    color_palette: str
    resolution: str
    compression: str
    scanner_model: str


class DocumentResponse(BaseModel):
    id: int
    file_url: str
    title: str
    heading: str
    author: str
    description_content: str
    dating: str
    legends: str
    format_doc: str
    color_palette: str
    resolution: str
    compression: str
    scanner_model: str
    created_at: datetime


class DocumentUpdateRequest(BaseModel):
    file_url: str | None
    title: str | None
    heading: str | None
    author: str | None
    description_content: str | None
    dating: str | None
    legends: str | None
    format_doc: str | None
    color_palette: str | None
    resolution: str | None
    compression: str | None
    scanner_model: str | None