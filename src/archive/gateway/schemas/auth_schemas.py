from pydantic import BaseModel, field_validator


class RegistrationForm(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str


class LoginForm(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_name: str
    user_role: str 

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
