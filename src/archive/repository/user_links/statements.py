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

delete_sci_council_group = text("""
    delete from scientific_council_group where
        "collection_id"=:collection_id
    AND
        "scientific_council_id"=:sci_council_id
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

delete_redactor_group = text("""
    delete from redactor_group where
        "collection_id"=:collection_id
    AND
        "redactor_id"=:redactor_id
""")
