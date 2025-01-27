from pydantic import BaseModel
from datetime import datetime
from typing import List

from .search_data_schemas import SearchDataRequest, SearchDataResponse, SearchDataUpdate


class DocumentRequest(BaseModel):
    author: str
    dating: str
    place_of_creating: str
    variety: str
    addressee: str
    brief_content: str
    case_prod_number: str
    main_text: str
    search_data: SearchDataRequest


class PhonoDocumentRequest(BaseModel):
    author: str
    dating: str
    place_of_creating: str
    genre: str
    brief_summary: str
    addressee: str 
    cypher: str
    lang: str 
    storage_media: str 


class DocumentResponse(BaseModel):
    id: str
    file_urls: List[str] | None
    author: str
    dating: str
    place_of_creating: str
    variety: str
    addressee: str
    brief_content: str
    case_prod_number: str
    main_text: str
    search_data: SearchDataResponse
    created_at: datetime
    type: str = "document"


class PhonoDocumentResponse(BaseModel):
    id: str 
    file_urls: List[str] | None 
    author: str
    dating: str
    place_of_creating: str
    genre: str
    brief_summary: str
    addressee: str 
    cypher: str
    lang: str 
    storage_media: str 
    created_at: datetime
    type: str = "phono_document"


class DocumentUpdateRequest(BaseModel):
    author: str | None
    dating: str | None
    place_of_creating: str | None
    variety: str | None
    addressee: str | None
    brief_content: str | None
    case_prod_number: str | None
    main_text: str | None
    search_data: SearchDataUpdate | None


class PhotoDocumentResponse(BaseModel):
    id: str


class VideoDocumentResponse(BaseModel):
    id: str
