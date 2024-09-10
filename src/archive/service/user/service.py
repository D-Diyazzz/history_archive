import jwt
import pytz

from pydantic import BaseModel
from datetime import datetime, timedelta

from src.archive.core import AbstractUnitOfWork
from src.archive.domains.user import User
from src.archive.config import SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRE, ACCESS_TOKEN_EXPIRE


class UserService:

    async def registration(
            self,
            data: BaseModel,
            uow: AbstractUnitOfWork,
    ):
        
        user = User.create(
            firstname=data.firstname,
            lastname=data.lastname,
            email=data.email,
            password=data.password
        )

        async with uow as uow:
            await uow.repository.add(user)
            await uow.commit()
        
        
    async def login(
            self,
            data: BaseModel,
            uow: AbstractUnitOfWork,
    ):
        
        async with uow as uow:
            user = await uow.repository.get_by_email(email=data.email)
            uow.commit()

        if user.verify_password(data.password) is False:
            raise Exception("Wrong password or email")
        
        data = dict(
            id=str(user.get_id),
            role=user.get_role.name,
            name=user.get_firstname,
        )
        
        access_token = self.__get_token(
            type='access', 
            payload=data, 
            ttl=int(ACCESS_TOKEN_EXPIRE),
            algorithm=ALGORITHM,
            key=SECRET_KEY
        )

        refresh_token = self.__get_token(
            type="refresh",
            payload=data,
            ttl=int(REFRESH_TOKEN_EXPIRE),
            algorithm=ALGORITHM,
            key=SECRET_KEY
        )

        return access_token, refresh_token, data
    
    async def refresh_token(
            self,
            data: AbstractUnitOfWork,
    ):
        try:
            data = jwt.decode(data.refresh_token, SECRET_KEY, algorithms=ALGORITHM)
            if data["type"] != "refresh":
                raise Exception("Autorization error")
        except jwt.exceptions.DecodeError:
            raise Exception("Authorization error")
        except jwt.exceptions.ExpiredSignatureError:
            raise Exception("Authorization error")

        data = dict(
            id=data["id"],
            role=data["role"],
            name=data["name"],
        )

        access_token = self.__get_token(
            type='access', 
            payload=data, 
            ttl=int(ACCESS_TOKEN_EXPIRE),
            algorithm=ALGORITHM,
            key=SECRET_KEY
        )

        refresh_token = self.__get_token(
            type="refresh",
            payload=data,
            ttl=int(REFRESH_TOKEN_EXPIRE),
            algorithm=ALGORITHM,
            key=SECRET_KEY
        )

        return access_token, refresh_token

        

    def __get_token(
            self,         
            type: str,
            payload: dict,
            ttl: int,
            algorithm: str,
            key: str
    ) -> str:
                
        data = dict(
            iss="e-collection@auth_service",
            type=type,
            exp=datetime.now(pytz.UTC) + timedelta(minutes=ttl)
        )

        payload.update(data)

        return jwt.encode(payload=payload, key=key, algorithm=algorithm)
