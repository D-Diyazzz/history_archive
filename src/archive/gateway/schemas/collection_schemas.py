from typing import List, Optional, Union
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

from src.archive.gateway.schemas.document_schemas import DocumentResponse, PhonoDocumentResponse, PhotoDocumentResponse, VideoDocumentResponse
from src.archive.gateway.schemas.user_schemas import UserResponse


class CollectionRequest(BaseModel):
    theme: str
    title: str


class CollectionResponse(BaseModel):
    id: str
    file_url: str
    html_url: str
    theme: str
    title: str
    author: UserResponse
    scientific_council_group: Optional[List[UserResponse]]
    redactor_group: Optional[List[UserResponse]]
    documents: Optional[List[Union[DocumentResponse, PhotoDocumentResponse, PhonoDocumentResponse, VideoDocumentResponse]]]
    is_approved: bool
    hash_code: str
    created_at: datetime
    activeEditor: Optional[UserResponse]


class CollectionEditRequest(BaseModel):
    theme: str
    title: str
    html_data: str


class CollectionPinDocumentRequest(BaseModel):
    doc_id: str
    doc_type: str
