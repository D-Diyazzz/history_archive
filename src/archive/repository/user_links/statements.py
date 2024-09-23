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
