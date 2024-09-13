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
        id,
        search_data_id,
        file_urls,
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
        :id,
        :search_data_id,
        :file_urls,
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
        file_urls=:file_urls,
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


insert_photo_document = text("""

    insert into photo_documents (
        search_data_id,
        file_urls,
        author,
        dating,
        place_of_creating,
        title,
        completeness_of_reproduction,
        storage_media,
        color,
        size_of_original,
        image_scale,
        created_at
    ) values (
        :search_data_id,
        :file_urls,
        :author,
        :dating,
        :place_of_creating,
        :title,
        :completeness_of_reproduction,
        :storage_media,
        :color,
        :size_of_original,
        :image_scale,
        :created_at
    ) returning id

""")

select_photo_document_by_id = text("""

    select 
        pd.*,
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
    from photo_documents pd
    join search_data s on pd.search_data_id = s.id
    where pd.id=:id

""")

select_photo_document = text("""

    select 
        pd.*,
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
    from photo_documents pd
    join search_data s on pd.search_data_id = s.id

""")

update_photo_document = text("""

    update photo_documents
    set
        file_urls=:file_urls,
        author=:author,
        dating=:dating,
        place_of_creating=:place_of_creating,
        title=:title,
        completeness_of_reproduction=:completeness_of_reproduction,
        storage_media=:storage_media,
        color=:color,
        size_of_original=:size_of_original,
        image_scale=:image_scale
    where id=:id

""")

delete_photo_document = text("""

    delete from photo_documents where id=:id

""")


insert_video_document = text("""

    insert into video_documents (
        search_data_id,
        file_urls,
        author,
        dating,
        place_of_creating,
        title,
        volume,
        num_of_parts,
        color,
        creator,
        info_of_publication,
        created_at
    ) values (
        :search_data_id,
        :file_urls,
        :author,
        :dating,
        :place_of_creating,
        :title,
        :volume,
        :num_of_parts,
        :color,
        :creator,
        :info_of_publication,
        :created_at
    ) returning id

""")

select_video_document_by_id = text("""

    select 
        vd.*,
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
    from video_documents vd
    join search_data s on vd.search_data_id = s.id
    where vd.id=:id

""")

select_video_document = text("""

    select 
        vd.*,
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
    from video_documents vd
    join search_data s on vd.search_data_id = s.id

""")

update_video_document = text("""

    update video_documents
    set
        file_urls=:file_urls,
        author=:author,
        dating=:dating,
        place_of_creating=:place_of_creating,
        title=:title,
        volume=:volume,
        num_of_parts=:num_of_parts,
        color=:color,
        creator=:creator,
        info_of_publication=:info_of_publication
    where id=:id

""")

delete_video_document = text("""

    delete from video_documents where id=:id

""")


insert_phono_document = text("""

    insert into phono_documents (
        file_urls,
        author,
        dating,
        place_of_creating,
        genre,
        brief_summary,
        addressee,
        cypher,
        lang,
        storage_media,
        created_at
    ) values (
        :file_urls,
        :author,
        :dating,
        :place_of_creating,
        :genre,
        :brief_summary,
        :addressee,
        :cypher,
        :lang,
        :storage_media,
        :created_at
    ) returning id

""")

select_phono_document_by_id = text("""

    select 
        pd.*
    from phono_documents pd
    where pd.id=:id

""")

select_phono_document = text("""

    select 
        pd.*
    from phono_documents pd

""")

update_phono_document = text("""

    update phono_documents
    set
        file_urls=:file_urls,
        author=:author,
        dating=:dating,
        place_of_creating=:place_of_creating,
        genre=:genre,
        brief_summary=:brief_summary,
        addressee=:addressee,
        cypher=:cypher,
        lang=:lang,
        storage_media=:storage_media
    where id=:id

""")

delete_phono_document = text("""

    delete from phono_documents where id=:id

""")

