import json

from src.archive.domains.document import Document, SearchData, PhotoDocument, VideoDocument, PhonoDocument


def search_data_to_dict(model: Document):
    model_dict = {
        "search_data_cypher": model.search_data.cypher if model.search_data and model.search_data.cypher else None,
        "search_data_fund": model.search_data.fund if model.search_data and model.search_data.fund else None,
        "search_data_inventory": model.search_data.inventory if model.search_data and model.search_data.inventory else None,
        "search_data_case": model.search_data.case if model.search_data and model.search_data.case else None,
        "search_data_leaf": model.search_data.leaf if model.search_data and model.search_data.leaf else None,
        "search_data_authenticity": model.search_data.authenticity if model.search_data and model.search_data.authenticity else None,
        "search_data_lang": model.search_data.lang if model.search_data and model.search_data.lang else None,
        "search_data_playback_method": model.search_data.playback_method if model.search_data and model.search_data.playback_method else None,
        "search_data_other": model.search_data.other if model.search_data and model.search_data.other else None,
    }

    return model_dict

def document_to_dict(model: Document):
    print(model.author)
    model_dict = {
        "file_urls": json.dumps(model.file_urls) if model.file_urls else None,
        "author": model.author if model.author else None,
        "dating": model.dating if model.dating else None,
        "place_of_creating": model.place_of_creating if model.place_of_creating else None,
        "variety": model.variety if model.variety else None,
        "addressee": model.addressee if model.addressee else None,
        "brief_content": model.brief_content if model.brief_content else None,
        "case_prod_number": model.case_prod_number if model.case_prod_number else None,
        "main_text": model.main_text if model.main_text else None,
        "created_at": model.created_at if model.created_at else None,
        "search_data_id": model.search_data.id if model.search_data and model.search_data.id else None,
    }

    return model_dict
    # return {k: v for k, v in model_dict.items() if v is not None}

def photo_document_to_dict(model):
    return {
        "file_urls": json.dumps(model.file_urls) if model.file_urls else None,
        "author": model.author if model.author else None,
        "dating": model.dating if model.dating else None,
        "place_of_creating": model.place_of_creating if model.place_of_creating else None,
        "title": model.title if model.title else None,
        "completeness_of_reproduction": model.completeness_of_reproduction if model.completeness_of_reproduction else None,
        "storage_media": model.storage_media if model.storage_media else None,
        "color": model.color if model.color else None,
        "size_of_original": model.size_of_original if model.size_of_original else None,
        "image_scale": model.image_scale if model.image_scale else None,
        "created_at": model.created_at if model.created_at else None,
        "search_data_id": model.search_data.id if model.search_data and model.search_data.id else None,
    }

def video_document_to_dict(model):
    return {
        "file_urls": json.dumps(model.file_urls) if model.file_urls else None,
        "author": model.author if model.author else None,
        "dating": model.dating if model.dating else None,
        "place_of_creating": model.place_of_creating if model.place_of_creating else None,
        "title": model.title if model.title else None,
        "volume": model.volume if model.volume else None,
        "num_of_parts": model.num_of_parts if model.num_of_parts else None,
        "color": model.color if model.color else None,
        "creator": model.creator if model.creator else None,
        "info_of_publication": model.info_of_publication if model.info_of_publication else None,
        "created_at": model.created_at if model.created_at else None,
        "search_data_id": model.search_data.id if model.search_data and model.search_data.id else None,
    }

def phono_document_to_dict(model):
    return {
        "file_urls": json.dumps(model.file_urls) if model.file_urls else None,
        "author": model.author if model.author else None,
        "dating": model.dating if model.dating else None,
        "place_of_creating": model.place_of_creating if model.place_of_creating else None,
        "genre": model.genre if model.genre else None,
        "brief_summary": model.brief_summary if model.brief_summary else None,
        "addressee": model.addressee if model.addressee else None,
        "cypher": model.cypher if model.cypher else None,
        "lang": model.lang if model.lang else None,
        "storage_media": model.storage_media if model.storage_media else None,
        "created_at": model.created_at if model.created_at else None
    }



def dict_to_document(data):
    search_data = SearchData(
        id=data.search_data_id,
        cypher=data.search_data_cypher,
        fund=data.search_data_fund,
        inventory=data.search_data_inventory,
        case=data.search_data_case,
        leaf=data.search_data_leaf,
        authenticity=data.search_data_authenticity,
        lang=data.search_data_lang,
        playback_method=data.search_data_playback_method,
        other=data.search_data_other
    )

    return Document(
        id=data.id,
        file_urls=data.file_urls,
        author=data.author,
        dating=data.dating,
        place_of_creating=data.place_of_creating,
        variety=data.variety,
        addressee=data.addressee,
        brief_content=data.brief_content,
        case_prod_number=data.case_prod_number,
        main_text=data.main_text,
        created_at=data.created_at,
        search_data=search_data
    )

def dict_to_photo_document(data):
    search_data = SearchData(
        id=data.search_data_id,
        cypher=data.search_data_cypher,
        fund=data.search_data_fund,
        inventory=data.search_data_inventory,
        case=data.search_data_case,
        leaf=data.search_data_leaf,
        authenticity=data.search_data_authenticity,
        lang=data.search_data_lang,
        playback_method=data.search_data_playback_method,
        other=data.search_data_other
    )

    return PhotoDocument(
        id=data.id,
        file_urls=data.file_urls,
        author=data.author,
        dating=data.dating,
        place_of_creating=data.place_of_creating,
        title=data.title,
        completeness_of_reproduction=data.completeness_of_reproduction,
        storage_media=data.storage_media,
        color=data.color,
        size_of_original=data.size_of_original,
        image_scale=data.image_scale,
        created_at=data.created_at,
        search_data=search_data
    )

def dict_to_video_document(data):
    search_data = SearchData(
        id=data.search_data_id,
        cypher=data.search_data_cypher,
        fund=data.search_data_fund,
        inventory=data.search_data_inventory,
        case=data.search_data_case,
        leaf=data.search_data_leaf,
        authenticity=data.search_data_authenticity,
        lang=data.search_data_lang,
        playback_method=data.search_data_playback_method,
        other=data.search_data_other
    )

    return VideoDocument(
        id=data.id,
        file_urls=data.file_urls,
        author=data.author,
        dating=data.dating,
        place_of_creating=data.place_of_creating,
        title=data.title,
        volume=data.volume,
        num_of_parts=data.num_of_parts,
        color=data.color,
        creator=data.creator,
        info_of_publication=data.info_of_publication,
        created_at=data.created_at,
        search_data=search_data
    )

def dict_to_phono_document(data):
    return PhonoDocument(
        id=data.id,
        file_urls=data.file_urls,
        author=data.author,
        dating=data.dating,
        place_of_creating=data.place_of_creating,
        genre=data.genre,
        brief_summary=data.brief_summary,
        addressee=data.addressee,
        cypher=data.cypher,
        lang=data.lang,
        storage_media=data.storage_media,
        created_at=data.created_at
    )

