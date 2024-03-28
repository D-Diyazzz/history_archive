from typing import Annotated

from fastapi import Depends

from src.archive.core import UnitOfWork
from src.archive.database.engine import get_session
from src.archive.repository.user import UserRepository
from src.archive.gateway.schemas import RegistrationForm, LoginForm, TokenResponse, RefreshTokenRequest
from src.archive.service.user import UserService


service = UserService()

async def registration_handler(data: RegistrationForm):
    
    await service.registration(data=data, uow=UnitOfWork(reposiotry=UserRepository, session_factory=get_session))

    return ["Registration Success"]


async def login_handler(data: LoginForm):

    access_token, refresh_token = await service.login(data=data, uow=UnitOfWork(reposiotry=UserRepository, session_factory=get_session))

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


async def refresh_token_handler(data: RefreshTokenRequest):
    access_token, refresh_token = await service.refresh_token(data=data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )