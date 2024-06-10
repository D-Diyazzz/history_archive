from pydantic import BaseModel


class SearchDataRequest(BaseModel):
    cypher: str
    fund: str
    inventory: str
    case: str
    leaf: str
    authenticity: str
    lang: str
    playback_method: str
    other: str = None


class SearchDataResponse(BaseModel):
    id: int
    cypher: str
    fund: str
    inventory: str
    case: str
    leaf: str
    authenticity: str
    lang: str
    playback_method: str
    other: str | None


class SearchDataUpdate(BaseModel):
    cypher: str | None
    fund: str | None
    inventory: str | None
    case: str | None
    leaf: str | None
    authenticity: str | None
    lang: str | None
    playback_method: str | None
    other: str | None