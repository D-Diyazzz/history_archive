import json

from src.archive.domains.document import Document, SearchData


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