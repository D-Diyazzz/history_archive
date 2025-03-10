from src.archive.domains.collection import Collection


def collection_to_dict(model: Collection):
    model_dict = {
        "id": model.id,
        "file_url": model.file_url,
        "html_url": model.html_url,
        "theme": model.theme,
        "title": model.title,
        "author_id": model.author_id,
        "hash_code": model.hash_code,
        "isbn_link": model.isbn_link,
        "description": model.description,
        "is_approved": model.is_approved,
        "created_at": model.created_at
    }

    return model_dict

def dict_to_collection(collection):
    return Collection(
        id=collection.id,
        file_url=collection.file_url,
        html_url=collection.html_url,
        theme=collection.theme,
        title=collection.title,
        author_id=collection.author_id,
        hash_code=collection.hash_code,
        isbn_link=collection.isbn_link,
        description=collection.description,
        is_approved=collection.is_approved,
        created_at=collection.created_at
    )
