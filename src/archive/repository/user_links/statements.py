from sqlalchemy import text


insert_sci_council_group = text("""
    insert into scientific_council_group (
        "collection_id",
        "scientific_council_id",
        "is_approved"
    ) values (
        :collection_id,
        :sci_council_id,
        :is_approved
    ) returning id
""")

select_sci_council_group_by_id = text("""
    select * from scientific_council_group where id=:id
""")

select_sci_council_group = text("""
    select * from scientific_council_group
""")

select_sci_council_group_by_coll_and_user_id = text("""
    select * from scientific_council_group where 
        collection_id=:collection_id
    AND
        scientific_council_id=:sci_council_id
""")

delete_sci_council_group = text("""
    delete from scientific_council_group where id=:id
""")

delete_sci_council_group_by_coll_and_user_id = text("""
    delete from scientific_council_group where
        collection_id=:collection_id
    AND
        scientific_council_id=:sci_council_id
""")

update_sci_council_group = text("""
    update scientific_council_group
    set 
        "is_approved"=:is_approved
    where 
        "collection_id"=:collection_id
        AND
        "scientific_council_id"=:sci_council_id
""")


insert_redactor_group = text("""
    insert into redactor_group(
        "collection_id",
        "redactor_id"
    ) values (
        :collection_id,
        :redactor_id
    ) returning id 
""")

select_redactor_group = text("""
    select * from redactor_group
""")

select_redactor_group_by_id = text("""
    select * from redactor_group where id=:id
""")

select_redactor_group_by_coll_and_user_id = text("""
    select * from redactor_group where 
        collection_id=:collection_id
    AND
        redactor_id=:redactor_id
""")

delete_redactor_group = text("""
    delete from redactor_group where id=:id
""")

exist_redactor_in_group = text("""
    SELECT EXISTS(
        SELECT 1
        FROM redactor_group
        WHERE collection_id=:collection_id AND redactor_id=:redactor_id
    )
""")

delete_redactor_group_by_coll_and_user_id = text("""
    delete from redactor_group where
        collection_id=:collection_id
    AND
        redactor_id=:redactor_id
""")
