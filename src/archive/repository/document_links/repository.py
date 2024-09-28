from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.archive.core import AbstractLinkRepository


class DocumentsLinkRepostiory(AbstractLinkRepository):
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, obj_id: str, related_obj_id: str, **kwargs) -> int:
        table_map = {
            "document": "document_links",
            "photo_document": "photo_document_links",
            "video_document": "video_document_links",
            "phono_document": "phono_document_links"
        }

        id_field_map = {
            "document": "document_id",
            "photo_document": "photo_document_id",
            "video_document": "video_document_id",
            "phono_document": "phono_document_id"
        }

        table_name = table_map.get(kwargs["doc_type"])
        id_field = id_field_map.get(kwargs["doc_type"])

        if table_name and id_field:
            insert_query = text(f"""
                INSERT INTO {table_name} (
                    "collection_id",
                    "{id_field}"
                ) VALUES (
                    :coll_id,
                    :doc_id
                ) RETURNING id
            """)

            id = await self.session.execute(
                insert_query,
                {
                    "coll_id": obj_id,
                    "doc_id": related_obj_id
                }
            )
            return id.scalar()  
        else:
            raise ValueError(f"document type {kwargs['doc_type']} doesn't exist")

    async def update(self, obj_id: str, related_obj_id: str, **kwargs):
        pass

    async def exist(self, obj_id:str, related_obj_id:str, **kwargs):
        pass

    async def delete(self, obj_id: str, related_obj_id: str, **kwargs) -> None:
        table_map = {
            "document": "document_links",
            "photo_document": "photo_document_links",
            "video_document": "video_document_links",
            "phono_document": "phono_document_links"
        }

        id_field_map = {
            "document": "document_id",
            "photo_document": "photo_document_id",
            "video_document": "video_document_id",
            "phono_document": "phono_document_id"
        }

        table_name = table_map.get(kwargs["doc_type"])
        id_field = id_field_map.get(kwargs["doc_type"])

        if table_name and id_field:
            delete_query = text(f"""
                DELETE FROM {table_name} 
                WHERE "collection_id" = :coll_id 
                AND "{id_field}" = :doc_id
            """)

            await self.session.execute(
                delete_query,
                {
                    "coll_id": obj_id,
                    "doc_id": related_obj_id
                }
            )
        else:
            raise ValueError(f"document type {kwargs['doc_type']} doesn't exist") 

