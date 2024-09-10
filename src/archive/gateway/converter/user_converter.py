from sqlalchemy import Row

from src.archive.gateway.schemas.user_schemas import UserResponse


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
