import pytz

from enum import Enum
from passlib.context import CryptContext
from datetime import datetime

from src.archive.core import AbstractBaseEntity


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Role(Enum):
    BasicUser = "BasicUser"
    AdminUser = "AdminUser"
    RedactorUser = "RedactorUser"


class User(AbstractBaseEntity):

    def __init__(
            self,
            firstname: str,
            lastname: str,
            email: str,
            password: str,
            id: int = None,
            role: Role = Role.RedactorUser,
            created_at: datetime = None,
    ):
        self._id = id
        self._firstname = firstname
        self._lastname = lastname
        self._email = email
        self._password = pwd_context.hash(password)
        self._role = role
        self._created_at = created_at if created_at else datetime.now(pytz.UTC)


    @property
    def get_id(self) -> int:
        return self._id
    
    @property
    def get_firstname(self) -> str:
        return self._firstname
    
    @property
    def get_lastname(self) -> str:
        return self._lastname
    
    @property
    def get_email(self) -> str:
        return self._email
    
    @property
    def get_password(self) -> str:
        return self._password
    
    @property
    def get_role(self) -> Role:
        return self._role
    
    @property
    def get_created_at(self) -> str:
        return self._created_at