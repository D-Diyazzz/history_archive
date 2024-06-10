from sqlalchemy import text
from typing import List

from src.archive.database.engine import AsyncEngine
from src.archive.gateway.converter import DocumentConverter
from src.archive.gateway.schemas import DocumentResponse


class DocumentViews:

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
        
        return DocumentConverter.row_to_document_list(documents=docs_row)