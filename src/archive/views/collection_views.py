from sqlalchemy import text
from typing import List

from src.archive.database.engine import AsyncEngine
from src.archive.gateway.converter.collection_converter import CollectionConverter
from src.archive.gateway.schemas import CollectionResponse
from src.archive.views.user_views import UserViews


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
            
            sci_council_group = await UserViews.get_sci_group_by_coll_id(coll_id=id, engine=engine)
            redactor_group = await UserViews.get_redactor_group_by_coll_id(coll_id=id, engine=engine)

            documents_row = (await conn.execute(
                text("""
                    SELECT d.*,
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

                    FROM documents d
                    JOIN document_links dl ON d.id = dl.document_id
                    JOIN search_data s on d.search_data_id = s.id
                    WHERE dl.collection_id = :collection_id
                """),{
                    "collection_id": id
                    }
                )).all()
            print(documents_row)
            photo_documents_row = (await conn.execute(
                text("""
                    SELECT pd.*
                    FROM photo_documents pd
                    JOIN photo_document_links pdl ON pd.id = pdl.photo_document_id
                    WHERE pdl.collection_id = :collection_id
                """),{
                    "collection_id": id
                    }
                )).all()

            video_documents_row = (await conn.execute(
                text("""
                    SELECT vd.*
                    FROM video_documents vd
                    JOIN video_document_links vdl ON vd.id = vdl.video_document_id
                    WHERE vdl.collection_id = :collection_id
                """),{
                    "collection_id": id
                    }
                )).all()

            phono_documents_row = (await conn.execute(
                text("""
                    SELECT phd.*
                    FROM phono_documents phd
                    JOIN phono_document_links phdl ON phd.id = phdl.phono_document_id
                    WHERE phdl.collection_id = :collection_id
                """),{
                    "collection_id": id
                    }
                )).all()

            return CollectionConverter.row_to_collection(collection=coll_row, documents=documents_row, sci_group=sci_council_group, redactor_group=redactor_group)

