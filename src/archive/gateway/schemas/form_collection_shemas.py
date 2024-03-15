from pydantic import BaseModel


class FormCollectionRequest(BaseModel):
    name: str


class FormCollectionResponse(BaseModel):
    id: int
    name: str