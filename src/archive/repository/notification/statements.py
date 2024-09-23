from sqlalchemy import text


insert_collection_notification = text("""
    insert into notification_collection(
        "collection_id",
        "user_id",
        "is_seen",
        "created_at"
    ) values (
        :collection_id,
        :user_id,
        :is_seen,
        :created_at
    ) returning id
""")

delete_collection_notification = text("""
    delete from notification_collection where id=:id
""")

select_collection_notification_by_id = text("""
    select * from notification_collection where id=:id
""")

update_collection_notification = text("""
    update notification_collection
    set 
        is_seen=:is_seen
    where id=:id
""")
