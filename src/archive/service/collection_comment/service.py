from uuid import UUID

from src.archive.core.unit_of_work import AbstractUnitOfWork2
from src.archive.domains.collection_comment import CollectionComment


class CollectionCommentService:

    async def edit_comment(
        self,
        user_id: UUID,
        coll_id: UUID,
        text: str,
        comment_id: int,
        uow: AbstractUnitOfWork2
    ):
        async with uow as uow:
            comment = await uow.get(comment_id, CollectionComment)
            if str(comment.collection_id) != str(coll_id) or str(comment.user_id) != str(user_id):
                uow.rollback()
                raise ValueError("Access denied")
            comment.update_text(new_text=text)
            await uow.update(comment)
            await uow.commit()
