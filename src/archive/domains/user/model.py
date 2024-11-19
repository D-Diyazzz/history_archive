import pytz

from enum import Enum
from passlib.context import CryptContext
from datetime import datetime
from uuid import UUID, uuid4

from src.archive.core import AbstractBaseEntity


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Role(Enum):
    BasicUser = "BasicUser"
    SuperAdminUser = "SuperAdminUser"
    AdminUser = "AdminUser"
    RedactorUser = "RedactorUser"
    ScientificCouncil = "ScientificCouncil"


class User(AbstractBaseEntity):

    _id: UUID | None
    _firstname: str
    _lastname: str
    _email: str
    _password: str
    _role: Role
    _created_at: datetime


    def __init__(
            self,
            id: UUID = None,
    ):
        self._id = id or uuid4()


    @classmethod    
    def create(
            cls,
            firstname: str,
            lastname: str,
            email: str,
            password: str,
    ):
        user = cls()
        user._firstname = firstname
        user._lastname = lastname
        user._email = email
        user._password = pwd_context.hash(password)
        user._role = Role.BasicUser
        user._created_at = datetime.now(pytz.UTC)
        return user
    
    @classmethod
    def upload(
        cls,
        firstname: str,
        lastname: str,
        email: str,
        password: str,
        id: str,
        role: Role,
        created_at: datetime,
    ):
        user = cls(id=id)
        user._firstname = firstname
        user._lastname = lastname
        user._email = email
        user._password = password
        user._role = role
        user._created_at = created_at
        return user

    @property
    def get_id(self) -> UUID:
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
    
    def verify_password(self, input_password: str) -> bool:
        return pwd_context.verify(input_password, self.get_password)

    def update_role(self, new_role):
        self._role = new_role
