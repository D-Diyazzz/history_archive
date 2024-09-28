from sqlalchemy import Row
from typing import List

from src.archive.gateway.schemas.user_schemas import UserResponse, SciUserReponse


class UserConverter:

    @classmethod
    def row_to_user(cls, user: Row) -> UserResponse:
        return UserResponse(
            id=str(user.id),
            firstname=user.firstname,
            lastname=user.lastname,
            role=user.role,
            email=user.email
        )

    @classmethod
    def row_to_user_list(cls, users: Row) -> List[UserResponse]:
        return [cls.row_to_user(user) for user in users]


    @classmethod
    def row_to_sci_user(cls, user: Row) -> SciUserReponse:
        return SciUserReponse(
            id=str(user.id),
            firstname=user.firstname,
            lastname=user.lastname,
            role=user.role,
            email=user.email,
            is_approved=user.is_approved
        )

    @classmethod
    def row_to_sci_user_list(cls, users: Row) -> List[SciUserReponse]:
        return [cls.row_to_sci_user(user) for user in users]
