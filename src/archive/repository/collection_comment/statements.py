from sqlalchemy import text


insert_collection_comment = text("""
    insert into collection_comment(
        "collection_id",
        "user_id",
        "text",
        "created_at"
    ) values (
        :collection_id,
        :user_id,
        :text,
        :created_at
    ) returning id 
""")

select_collection_comment = text("""
    select * from collection_comment
""")

select_collection_comment_by_id = text("""
    select * from collection_comment where id=:id
""")

update_collection_comment = text("""
    update collection_comment
    set 
        collection_id=:collection_id,
        user_id=:user_id,
        text=:text
    where id=:id
""")

delete_collection_comment = text("""
    delete from collection_comment where id=:id
""")

delete_collection_comment_by_coll_and_user_id = text("""
    delete from collection_comment where
        collection_id=:coll_id 
    AND 
        user_id=:user_id
""")
