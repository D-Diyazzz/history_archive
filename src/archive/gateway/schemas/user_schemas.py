from pydantic import BaseModel


class UserResponse(BaseModel):
    id: str
    firstname: str
    lastname: str
    role: str
    email: str


class SciUserReponse(UserResponse):
    is_approved: bool


class UserChangeRoleRequest(BaseModel):
    new_role: str
