from src.archive.domains.collection_comment import CollectionComment


def collection_comment_to_dict(model: CollectionComment):
    model_dict = {
        "id": model.id,
        "collection_id": model.collection_id,
        "user_id": model.user_id,
        "text": model.text,
        "created_at": model.created_at
    }
    return model_dict

def dict_to_collection_comment(coll_comment):
    return CollectionComment(
        id=coll_comment.id,
        collection_id=coll_comment.collection_id,
        user_id=coll_comment.user_id,
        text=coll_comment.text,
        created_at=coll_comment.created_at
    )
