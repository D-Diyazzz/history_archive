from pydantic import BaseModel
from datetime import datetime


class CollectionRequest(BaseModel):
    file_url: str
    theme: str
    purpose: str
    task: str
    type_coll_id: int
    class_coll_id: int
    format_coll_id: int
    method_coll_id: int
    preface: str | None
    note: str | None
    indication: str | None
    intro_text: str | None
    recommendations: str | None


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
    file_url: str
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
