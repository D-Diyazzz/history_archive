from src.archive.domains.collection import Collection, Class, Type, Format, Method


def collection_to_dict(model: Collection):
    model_dict = {
        "file_url": model.get_file_url if model.get_file_url else None,
        "theme": model.get_theme if model.get_theme else None,
        "purpose": model.get_purpose if model.get_purpose else None,
        "task": model.get_task if model.get_task else None,
        "type_id": model.get_type_coll.id if model.get_type_coll.id else None,
        "class_id": model.get_class_coll.id if model.get_class_coll.id else None,
        "format_id": model.get_format_coll.id if model.get_format_coll.id else None,
        "method_id": model.get_method_coll.id if model.get_method_coll.id else None,
        "preface": model.get_preface if model.get_preface else None,
        "note": model.get_note if model.get_note else None,
        "indication": model.get_indication if model.get_indication else None,
        "intro_text": model.get_intro_text if model.get_intro_text else None,
        "recommendations": model.get_recommendations if model.get_recommendations else None,
        "created_at": model.get_created_at if model.get_created_at else None,
    }

    return {k: v for k, v in model_dict.items() if v is not None}


def dict_to_collection(collection, type_coll, class_coll, format_coll, method_coll):
    return Collection(
        id=collection.id,
        file_url=collection.file_url,
        theme=collection.theme,
        purpose=collection.purpose,
        task=collection.task,
        type_coll=Type(
            id=type_coll.id,
            name=type_coll.name
        ),
        class_coll=Class(
            id=class_coll.id,
            name=class_coll.name
        ),
        format_coll=Format(
            id=format_coll.id,
            name=format_coll.name
        ),
        method_coll=Method(
            id=method_coll.id,
            name=method_coll.name
        ),
        preface=collection.preface,
        note=collection.note,
        indication=collection.indication,
        intro_text=collection.intro_text,
        recommendations=collection.recommendations,
        created_at=collection.created_at
    )