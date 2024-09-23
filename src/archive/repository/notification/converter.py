from src.archive.domains.notification import CollectionNotification


def collection_notification_to_dict(model: CollectionNotification):
    model_dict = {
        "id": model.id,
        "collection_id": model.collection_id,
        "user_id": model.user_id,
        "is_seen": model.is_seen,
        "created_at": model.created_at
    }
    return model_dict


def dict_to_collection_notification(notification):
    return CollectionNotification(
        id=notification.id,
        collection_id=notification.collection_id,
        user_id=notification.user_id,
        is_seen=notification.is_seen,
        created_at=notification.created_at
    )
