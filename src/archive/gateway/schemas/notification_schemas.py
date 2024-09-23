from pydantic import BaseModel
from datetime import datetime


class NotificationAddToCollectionResponse(BaseModel):
    id: int
    coll_id: str
    user_id: str
    is_seen: bool
    created_at: datetime
