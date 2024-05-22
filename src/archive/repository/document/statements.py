from sqlalchemy import text


insert_search_data = text("""

    insert into search_data (
                "cypher",
                "fund",
                "inventory",
                "case",
                "leaf",
                "authenticity",
                "lang",
                "playback_method",
                "other"
    ) values (
                :search_data_cypher,
                :search_data_fund,
                :search_data_inventory,
                :search_data_case,
                :search_data_leaf,
                :search_data_authenticity,
                :search_data_lang,
                :search_data_playback_method,
                :search_data_other
    ) returning id

""")


insert_document = text("""

    insert into documents (
        search_data_id,
        file_url,
        author,
        dating,
        place_of_creating,
        variety,
        addressee,
        brief_content,
        case_prod_number,
        main_text,
        created_at
    ) values (
        :search_data_id,
        :file_url,
        :author,
        :dating,
        :place_of_creating,
        :variety,
        :addressee,
        :brief_content,
        :case_prod_number,
        :main_text,
        :created_at
    ) returning id

""")


select_document_by_id = text("""

    select 
        d.*,
        s.id as search_data_id,
        s.cypher as search_data_cypher,
        s.fund as search_data_fund,
        s.inventory as search_data_inventory,
        s.case as search_data_case,
        s.leaf as search_data_leaf,
        s.authenticity as search_data_authenticity,
        s.lang as search_data_lang,
        s.playback_method as search_data_playback_method,
        s.other as search_data_other
    from documents d
    join search_data s on d.search_data_id = s.id
    where d.id=:id

""")

select_document = text("""

    select 
        d.*,
        s.id as search_data_id,
        s.cypher as search_data_cypher,
        s.fund as search_data_fund,
        s.inventory as search_data_inventory,
        s.case as search_data_case,
        s.leaf as search_data_leaf,
        s.authenticity as search_data_authenticity,
        s.lang as search_data_lang,
        s.playback_method as search_data_playback_method,
        s.other as search_data_other
    from documents d
    join search_data s on d.search_data_id = s.id

""")

update_document = text("""

    update documents
    set
        file_url=:file_url,
        author=:author,
        dating=:dating,
        place_of_creating=:place_of_creating,
        variety=:variety,
        addressee=:addressee,
        brief_content=:brief_content,
        case_prod_number=:case_prod_number,
        main_text=:main_text
    where id=:id

""")


update_search_data = text("""

    update search_data
    set
        cypher=:search_data_cypher,
        fund=:search_data_fund,
        inventory=:search_data_inventory,
        "case"=:search_data_case,
        leaf=:search_data_leaf,
        authenticity=:search_data_authenticity,
        lang=:search_data_lang,
        playback_method=:search_data_playback_method,
        other=:search_data_other
    where id=:id

""")


delete_search_data = text("""

    delete from search_data where id=:id

""")