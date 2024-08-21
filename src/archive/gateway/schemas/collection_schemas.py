from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class CollectionRequest(BaseModel):
    theme: str
    title: str
    author_id: UUID


class CollectionResponse(BaseModel):
    id: int
    file_url: str
    theme: str
    purpose: str
    task: str
    type_coll: str
    class_coll: str
    format_coll: str
    method_coll: str
    preface: str | None
    note: str | None
    indication: str | None
    intro_text: str | None
    recommendations: str | None
    created_at: datetime


class CollectionUpdateRequest(BaseModel):
    file_url: str | None
    theme: str | None
    purpose: str | None
    task: str | None
    type_coll_id: int | None
    class_coll_id: int | None
    format_coll_id: int | None
    method_coll_id: int | None
    preface: str | None
    note: str | None
    indication: str | None
    intro_text: str | None
    recommendations: str | None
