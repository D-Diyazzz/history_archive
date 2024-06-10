from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.archive.core import UnitOfWork
from src.archive.database.engine import get_session
from src.archive.repository.user import UserRepository
from src.archive.gateway.schemas import RegistrationForm, LoginForm, TokenResponse, RefreshTokenRequest, LoginResponse
from src.archive.service.user import UserService


service = UserService()

async def registration_handler(data: RegistrationForm):
    
    try:
        await service.registration(data=data, uow=UnitOfWork(reposiotry=UserRepository, session_factory=get_session))
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail="email exist")

    return ["Registration Success"]


async def login_handler(data: LoginForm):
    try:
        access_token, refresh_token, user_data = await service.login(data=data, uow=UnitOfWork(reposiotry=UserRepository, session_factory=get_session))
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e))

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_name=user_data["name"],
        user_role=user_data["role"]
    )


async def refresh_token_handler(data: RefreshTokenRequest):
    access_token, refresh_token = await service.refresh_token(data=data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )
