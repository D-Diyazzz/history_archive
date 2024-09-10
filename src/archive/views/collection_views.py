from sqlalchemy import text
from typing import List

from src.archive.database.engine import AsyncEngine
from src.archive.gateway.converter.collection_converter import CollectionConverter
from src.archive.gateway.schemas import CollectionResponse


class CollectionViews:

    @classmethod
    async def get_collection_by_id_view(
        cls,
        id: str,
        engine: AsyncEngine
    ) -> CollectionResponse:
        async with engine.begin() as conn:
            coll_row = (await conn.execute(
                text("""
                    select 
                        c.*,
                        u.id as user_id,
                        u.firstname as user_firstname,
                        u.lastname as user_lastname,
                        u.email as user_email,
                        u.role as user_role
                    from collection c 
                    join "user" u on c.author_id = u.id
                    where c.id=:id
                """),{
                    "id": id
                }
            )).one()
            
            sci_council_group_row = (await conn.execute(
                text("""
                    SELECT u.*
                        FROM "user" u
                    JOIN scientific_council_group scg ON u.id = scg.scientific_council_id
                    WHERE scg.collection_id = :id
                """),{
                    "id": id
                }
            )).all()

            redactor_group_row = (await conn.execute(
                text("""
                    SELECT u.*
                        FROM "user" u
                    JOIN redactor_group rg ON u.id = rg.redactor_id
                    WHERE rg.collection_id = :id
                """), {
                    "id": id
                }
            ))

            documents_row = (await conn.execute(
                text("""
                    SELECT d.*
                    FROM documents d
                    JOIN document_links dl ON d.id = dl.document_id
                    WHERE dl.collection_id = :collection_id
                """),{
                    "collection_id": id
                    }
                ))

            photo_documents_row = (await conn.execute(
                text("""
                    SELECT pd.*
                    FROM photo_documents pd
                    JOIN photo_document_links pdl ON pd.id = pdl.photo_document_id
                    WHERE pdl.collection_id = :collection_id
                """),{
                    "collection_id": id
                    }
                ))

            video_documents_row = (await conn.execute(
                text("""
                    SELECT vd.*
                    FROM video_documents vd
                    JOIN video_document_links vdl ON vd.id = vdl.video_document_id
                    WHERE vdl.collection_id = :collection_id
                """),{
                    "collection_id": id
                    }
                ))

            phono_documents_row = (await conn.execute(
                text("""
                    SELECT phd.*
                    FROM phono_documents phd
                    JOIN phono_document_links phdl ON phd.id = phdl.phono_document_id
                    WHERE phdl.collection_id = :collection_id
                """),{
                    "collection_id": id
                    }
                ))

            return CollectionConverter.row_to_collection(collection=coll_row)

