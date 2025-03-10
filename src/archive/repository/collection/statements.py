from sqlalchemy import text


insert_collection = text("""
    insert into collection(
        "id",
        "file_url",
        "html_url",
        "theme",
        "title",
        "author_id",
        "hash_code",
        "isbn_link",
        "description",
        "is_approved",
        "created_at"
    ) values (
        :id,
        :file_url,
        :html_url,
        :theme,
        :title,
        :author_id,
        :hash_code,
        :isbn_link,
        :description,
        :is_approved,
        :created_at
    ) returning id
""")

select_collection = text("""
    select 
        id,
        file_url,
        html_url,
        theme,
        title,
        author_id,
        hash_code,
        isbn_link,
        description,
        is_approved,
        created_at
    from collection
""")

select_collection_by_id = text("""
    select 
        id,
        file_url,
        html_url,
        theme,
        title,
        author_id,
        hash_code,
        isbn_link,
        description,
        is_approved,
        created_at
    from collection where id=:id
""")

update_collection = text("""
    update collection
    set 
        theme=:theme,
        title=:title,
        is_approved=:is_approved,
        isbn_link=:isbn_link,
        description=:description
    where id=:id
""")

delete_collection = text("""
    delete from collection where id=:id
""")
