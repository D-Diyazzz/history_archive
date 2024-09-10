from sqlalchemy import Row

from src.archive.gateway.schemas.collection_schemas import CollectionResponse
from src.archive.gateway.schemas.user_schemas import UserResponse


class CollectionConverter:

    @classmethod
    def row_to_collection(cls, collection: Row) -> CollectionResponse:
        return CollectionResponse(
            id=str(collection.id),
            file_url=collection.file_url,
            html_url=collection.html_url,
            theme=collection.theme,
            title=collection.title,
            author=UserResponse(
                id=str(collection.user_id),
                firstname=collection.user_firstname,
                lastname=collection.user_lastname,
                role=collection.user_role,
                email=collection.user_email
            ),
            scientific_council_group=None,
            redactor_group=None,
            documents=None,
            is_approved=collection.is_approved,
            hash_code=collection.hash_code,
            created_at=collection.created_at,
            activeEditor=None
        )
