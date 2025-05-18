from sqlalchemy import text
from typing import List

from src.archive.database.engine import AsyncEngine
from src.archive.gateway.converter import DocumentConverter
from src.archive.gateway.converter.document_converter import PhonoDocumentConverter, PhotoDocumentConverter, VideoDocumentConverter
from src.archive.gateway.schemas import DocumentResponse
from src.archive.gateway.schemas.document_schemas import PhonoDocumentResponse, PhotoDocumentResponse, VideoDocumentResponse


class DocumentViews:

    @classmethod
    async def get_all_documents_view(
        cls,
        engine: AsyncEngine
    ) -> List:
        all_documents = []
        documents = await DocumentViews.get_documents_view(engine)
        phono_documents = await DocumentViews.get_phono_document(engine)
        photo_documents = await DocumentViews.get_photo_documents_view(engine)
        video_documents = await DocumentViews.get_video_documents_view(engine)

        # Объединяем
        all_documents.extend(documents)
        all_documents.extend(photo_documents)
        all_documents.extend(video_documents)
        all_documents.extend(phono_documents)

        # Сортируем по дате создания (сначала новые)
        all_documents = sorted(all_documents, key=lambda x: x.created_at, reverse=True)

        return all_documents

    @classmethod
    async def get_document_by_id_view(
            cls,
            id: int,
            engine: AsyncEngine
    ) -> DocumentResponse:
        async with engine.begin() as conn:
            doc_row = (await conn.execute(
                text("""
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
                """), {
                    "id": id
                }
            )).one()

        return DocumentConverter.row_to_document(document=doc_row)

    @classmethod
    async def get_documents_view(
            cls,
            engine: AsyncEngine
    ) -> List[DocumentResponse]:
        async with engine.begin() as conn:
            docs_row = (await conn.execute(
                text("""
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
            )).all()
        
        documents = DocumentConverter.row_to_document_list(documents=docs_row)
        return documents[::-1]


    @classmethod
    async def get_phono_document_by_id_view(
            cls,
            id: str,
            engine: AsyncEngine
    ) -> PhonoDocumentResponse:
        async with engine.begin() as conn:
            doc_row = (await conn.execute(
                text("""
                    select
                        *
                    from phono_documents d 
                    where d.id=:id
                """),{
                    "id": id
                }
            )).one() 

        return PhonoDocumentConverter.row_to_document(doc_row)

    @classmethod
    async def get_phono_document(
        cls,
        engine: AsyncEngine
    ) -> List[PhonoDocumentResponse]:
        async with engine.begin() as conn:
            docs_row = (await conn.execute(
                text("""
                    select
                        *
                    from phono_documents
                """)
            )).all()
        
        documents = PhonoDocumentConverter.row_to_document_list(documents=docs_row)
        return documents[::-1]



    @classmethod
    async def get_video_document_by_id_view(
            cls,
            id: int,
            engine: AsyncEngine
    ) -> VideoDocumentResponse:
        async with engine.begin() as conn:
            doc_row = (await conn.execute(
                text("""
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
                    from video_documents d
                    join search_data s on d.search_data_id = s.id
                    where d.id = :id
                """), {"id": id}
            )).one()

        return VideoDocumentConverter.row_to_document(document=doc_row)


    @classmethod
    async def get_video_documents_view(
            cls,
            engine: AsyncEngine
    ) -> List[VideoDocumentResponse]:
        async with engine.begin() as conn:
            docs_row = (await conn.execute(
                text("""
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
                    from video_documents d
                    join search_data s on d.search_data_id = s.id
                """)
            )).all()

        documents = VideoDocumentConverter.row_to_document_list(docs_row)
        return documents[::-1]


    @classmethod
    async def get_photo_document_by_id_view(
            cls,
            id: int,
            engine: AsyncEngine
    ) -> PhotoDocumentResponse:
        async with engine.begin() as conn:
            doc_row = (await conn.execute(
                text("""
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
                    from photo_documents d
                    join search_data s on d.search_data_id = s.id
                    where d.id = :id
                """), {"id": id}
            )).one()

        return PhotoDocumentConverter.row_to_document(document=doc_row)


    @classmethod
    async def get_photo_documents_view(
            cls,
            engine: AsyncEngine
    ) -> List[PhotoDocumentResponse]:
        async with engine.begin() as conn:
            docs_row = (await conn.execute(
                text("""
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
                    from photo_documents d
                    join search_data s on d.search_data_id = s.id
                """)
            )).all()

        documents = PhotoDocumentConverter.row_to_document_list(docs_row)
        return documents[::-1]

