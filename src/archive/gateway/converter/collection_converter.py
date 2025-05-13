from typing import List
from pydantic import BaseModel
from sqlalchemy import Row

from src.archive.gateway.converter.document_converter import DocumentConverter, PhonoDocumentConverter, PhotoDocumentConverter, VideoDocumentConverter
from src.archive.gateway.schemas.collection_schemas import CollectionResponse, CollectionCommentResponse, CollectionShortResponse
from src.archive.gateway.schemas.user_schemas import UserResponse


class CollectionConverter:

    @classmethod
    def row_to_collection(
            cls, 
            collection: Row,
            documents: Row,
            sci_group: BaseModel,
            redactor_group: BaseModel,
            video_documents: Row, 
            photo_documents: Row,
            phono_documents: Row
        ) -> CollectionResponse:
        documents_res = DocumentConverter.row_to_document_list(documents=documents)
        video_documents_res = VideoDocumentConverter.row_to_document_list(documents=video_documents)
        photo_documents_res = PhotoDocumentConverter.row_to_document_list(documents=photo_documents)
        phono_documents_res = PhonoDocumentConverter.row_to_document_list(documents=phono_documents)

        all_documents = (
            documents_res +
            video_documents_res +
            photo_documents_res +
            phono_documents_res
        )

        all_documents_sorted = sorted(all_documents, key=lambda x: x.created_at, reverse=True)

        return CollectionResponse(
            id=str(collection.id),
            file_url=collection.file_url,
            html_url=collection.html_url,
            theme=collection.theme,
            title=collection.title,
            isbn_link=collection.isbn_link,
            description=collection.description,
            author=UserResponse(
                id=str(collection.user_id),
                firstname=collection.user_firstname,
                lastname=collection.user_lastname,
                role=collection.user_role,
                email=collection.user_email
            ),
            scientific_council_group=sci_group,
            redactor_group=redactor_group,
            documents=all_documents_sorted,
            is_approved=collection.is_approved,
            hash_code=collection.hash_code,
            created_at=collection.created_at,
            activeEditor=None
        )

    @classmethod
    def row_to_collection_comment(
        cls,
        comment: Row
    ) -> CollectionCommentResponse:
        return CollectionCommentResponse(
            id=comment.id,
            collection_id=str(comment.collection_id),
            user_id=str(comment.user_id),
            text=comment.text,
            created_at=comment.created_at
        )

    
    @classmethod
    def row_to_collection_short(
        cls,
        collection: Row
    ) ->  CollectionShortResponse:
        return CollectionShortResponse(
            id=str(collection.id),
            file_url=collection.file_url,
            html_url=collection.html_url,
            theme=collection.theme,
            title=collection.title,
            isbn_link=collection.isbn_link,
            description=collection.description,
            author=UserResponse(
                id=str(collection.user_id),
                firstname=collection.user_firstname,
                lastname=collection.user_lastname,
                role=collection.user_role,
                email=collection.user_email
            ),
            is_approved=collection.is_approved,
            hash_code=collection.hash_code,
            created_at=collection.created_at,
        )

    
    @classmethod
    def row_to_collection_short_list(
        cls,
        collections: Row
    ) -> List[CollectionShortResponse]:
        return [cls.row_to_collection_short(coll) for coll in collections]
