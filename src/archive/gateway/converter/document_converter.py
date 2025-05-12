from sqlalchemy import Row
from typing import List

from src.archive.domains.document.phono_document import PhonoDocument
from src.archive.domains.document.photo_document_model import PhotoDocument
from src.archive.domains.document.video_documents_model import VideoDocument
from src.archive.gateway.schemas import DocumentResponse, SearchDataResponse
from src.archive.domains.document import Document
from src.archive.gateway.schemas.document_schemas import PhonoDocumentResponse, PhotoDocumentResponse, VideoDocumentResponse

class DocumentConverter:
    
    @classmethod
    def row_to_document(cls, document: Row) -> DocumentResponse:
        return DocumentResponse(
            id=str(document.id),
            file_urls=document.file_urls if document.file_urls else None,
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
        return [cls.row_to_document(doc) for doc in documents]


    @classmethod
    def model_to_document(cls, document: Document) -> DocumentResponse:
        return DocumentResponse(
        id=str(document.id),
        file_urls=document.file_urls if document.file_urls else None,
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


class PhonoDocumentConverter:

    @classmethod
    def row_to_document(cls, document: Row) -> PhonoDocumentResponse:
        return PhonoDocumentResponse(
            id=str(document.id),
            file_urls=document.file_urls if document.file_urls else None,
            author=document.author,
            dating=document.dating,
            place_of_creating=document.place_of_creating,
            genre=document.genre,
            brief_summary=document.brief_summary,
            addressee=document.addressee,
            cypher=document.cypher,
            lang=document.lang,
            storage_media=document.storage_media,
            created_at=document.created_at
        )

    @classmethod
    def row_to_document_list(cls, documents) -> List[DocumentResponse]:
        return [cls.row_to_document(doc) for doc in documents]


    @classmethod
    def model_to_document(cls, document: PhonoDocument) -> PhonoDocumentResponse:
        return PhonoDocumentResponse(
            id=str(document.id),
            file_urls=document.file_urls if document.file_urls else None,
            author=document.author,
            dating=document.dating,
            place_of_creating=document.place_of_creating,
            genre=document.genre,
            brief_summary=document.brief_summary,
            addressee=document.addressee,
            cypher=document.cypher,
            lang=document.lang,
            storage_media=document.storage_media,
            created_at=document.created_at
        )

    @classmethod
    def model_to_document_list(cls, documents: List[PhonoDocument]) -> List[DocumentResponse]:
        return [cls.row_to_document(doc) for doc in documents]

 
 
 
class PhotoDocumentConverter:

    @classmethod
    def row_to_document(cls, document: Row) -> PhotoDocumentResponse:
        return PhotoDocumentResponse(
            id=str(document.id),
            file_urls=document.file_urls if document.file_urls else None,
            author=document.author,
            dating=document.dating,
            place_of_creating=document.place_of_creating,
            title=document.title,
            completeness_of_reproduction=document.completeness_of_reproduction,
            storage_media=document.storage_media,
            color=document.color,
            size_of_original=document.size_of_original,
            image_scale=document.image_scale,
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
            created_at=document.created_at,
            type="photo_document"
        )

    @classmethod
    def row_to_document_list(cls, documents) -> List[PhotoDocumentResponse]:
        return [cls.row_to_document(doc) for doc in documents]

    @classmethod
    def model_to_document(cls, document: PhotoDocument) -> PhotoDocumentResponse:
        return PhotoDocumentResponse(
            id=str(document.id),
            file_urls=document.file_urls if document.file_urls else None,
            author=document.author,
            dating=document.dating,
            place_of_creating=document.place_of_creating,
            title=document.title,
            completeness_of_reproduction=document.completeness_of_reproduction,
            storage_media=document.storage_media,
            color=document.color,
            size_of_original=document.size_of_original,
            image_scale=document.image_scale,
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
            created_at=document.created_at,
            type="photo_document"
        )

    @classmethod
    def model_to_document_list(cls, documents: List[PhotoDocument]) -> List[PhotoDocumentResponse]:
        return [cls.model_to_document(doc) for doc in documents]



class VideoDocumentConverter:

    @classmethod
    def row_to_document(cls, document: Row) -> VideoDocumentResponse:
        return VideoDocumentResponse(
            id=str(document.id),
            file_urls=document.file_urls if document.file_urls else None,
            author=document.author,
            dating=document.dating,
            place_of_creating=document.place_of_creating,
            title=document.title,
            volume=document.volume,
            num_of_parts=document.num_of_parts,
            color=document.color,
            creator=document.creator,
            info_of_publication=document.info_of_publication,
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
            created_at=document.created_at,
            type="video_document"
        )

    @classmethod
    def row_to_document_list(cls, documents) -> List[VideoDocumentResponse]:
        return [cls.row_to_document(doc) for doc in documents]

    @classmethod
    def model_to_document(cls, document: VideoDocument) -> VideoDocumentResponse:
        return VideoDocumentResponse(
            id=str(document.id),
            file_urls=document.file_urls if document.file_urls else None,
            author=document.author,
            dating=document.dating,
            place_of_creating=document.place_of_creating,
            title=document.title,
            volume=document.volume,
            num_of_parts=document.num_of_parts,
            color=document.color,
            creator=document.creator,
            info_of_publication=document.info_of_publication,
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
            created_at=document.created_at,
            type="video_document"
        )

    @classmethod
    def model_to_document_list(cls, documents: List[VideoDocument]) -> List[VideoDocumentResponse]:
        return [cls.model_to_document(doc) for doc in documents]

