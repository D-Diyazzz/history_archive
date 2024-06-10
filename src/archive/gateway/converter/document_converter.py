from sqlalchemy import Row
from typing import List

from src.archive.gateway.schemas import DocumentResponse, SearchDataResponse
from src.archive.domains.document import Document

class DocumentConverter:

    @classmethod
    def row_to_document(cls, document: Row) -> DocumentResponse:
        return DocumentResponse(
            id=document.id,
            file_urls=document.file_urls,
            author=document.author,
            dating=document.dating,
            place_of_creating=document.place_of_creating,
            variety=document.variety,
            addressee=document.addressee,
            brief_content=document.brief_content,
            case_prod_number=document.case_prod_number,
            main_text=document.main_text,
            search_data=SearchDataResponse(
                id=document.search_data_id,
                cypher=document.search_data_cypher,
                fund=document.search_data_fund,
                inventory=document.search_data_inventory,
                case=document.search_data_case,
                leaf=document.search_data_leaf,
                authenticity=document.search_data_authenticity,
                lang=document.search_data_lang,
                playback_method=document.search_data_playback_method,
                other=document.search_data_other
            ),
            created_at=document.created_at
        )
    
    @classmethod
    def row_to_document_list(cls, documents) -> List[DocumentResponse]:
        print(type(documents))
        return [cls.row_to_document(doc) for doc in documents]


    @classmethod
    def model_to_document(cls, document: Document) -> DocumentResponse:
        return DocumentResponse(
        id=document.id,
        file_urls=document.file_urls,
        author=document.author,
        dating=document.dating,
        place_of_creating=document.place_of_creating,
        variety=document.variety,
        addressee=document.addressee,
        brief_content=document.brief_content,
        case_prod_number=document.case_prod_number,
        main_text=document.main_text,
        search_data=SearchDataResponse(
            id=document.search_data.id,
            cypher=document.search_data.cypher,
            fund=document.search_data.fund,
            inventory=document.search_data.inventory,
            case=document.search_data.case,
            leaf=document.search_data.leaf,
            authenticity=document.search_data.authenticity,
            lang=document.search_data.lang,
            playback_method=document.search_data.playback_method,
            other=document.search_data.other
        ),
        created_at=document.created_at
    )


    @classmethod
    def model_to_document_list(cls, documents: List[Document]) -> List[Document]:
        return [cls.model_to_document(doc) for doc in documents]