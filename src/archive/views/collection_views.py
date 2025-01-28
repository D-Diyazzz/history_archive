from sqlalchemy import text
from typing import List

from src.archive.database.engine import AsyncEngine
from src.archive.gateway.converter.collection_converter import CollectionConverter
from src.archive.gateway.schemas import CollectionResponse, CollectionShortResponse
from src.archive.gateway.schemas.collection_schemas import CollectionCommentResponse
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


    @classmethod
    async def get_user_comment(
        cls,
        coll_id: str,
        user_id: str,
        engine: AsyncEngine
    ):
        async with engine.begin() as conn:
            comment_row = (await conn.execute(
                text("""
                    select * from collection_comment where
                        collection_id=:collection_id
                    AND
                        user_id=:user_id
                """),{
                    "collection_id": coll_id,
                    "user_id": user_id
                }
            )).one()

        return CollectionConverter.row_to_collection_comment(comment=comment_row)


    @classmethod
    async def get_collection_by_user_id_admin(
        cls,
        id: str,
        engine: AsyncEngine
    ) -> List[CollectionShortResponse]:
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
                    where u.id=:id
                """),{
                    "id": id
                }
            )).all()

        collections = CollectionConverter.row_to_collection_short_list(collections=coll_row)
        collections = sorted(collections, key=lambda x: x.created_at, reverse=True)

        return collections

    @classmethod
    async def get_collection_by_user_id_sci(
        cls,
        id: str,
        engine: AsyncEngine
    ) -> List[CollectionShortResponse]:
        async with engine.begin() as conn:
            coll_row = (await conn.execute(
                text("""
                    SELECT 
                        c.*, 
                        u.id as user_id,
                        u.firstname as user_firstname,
                        u.lastname as user_lastname,
                        u.email as user_email,
                        u.role as user_role
                    FROM collection c
                    JOIN scientific_council_group sci_u 
                      ON sci_u.collection_id = c.id
                    JOIN "user" u
                      ON u.id = c.author_id
                    WHERE sci_u.scientific_council_id = :id;

                """),{
                    "id": id
                    }
            )).all()

        collections = CollectionConverter.row_to_collection_short_list(collections=coll_row)
        collections = sorted(collections, key=lambda x: x.created_at, reverse=True)
        return collections


    @classmethod
    async def get_collection_by_user_id_redactor(
        cls,
        id: str,
        engine: AsyncEngine
    ) -> List[CollectionShortResponse]:
        async with engine.begin() as conn:
            coll_row = (await conn.execute(
                text("""
                    SELECT 
                        c.*, 
                        u.id as user_id,
                        u.firstname as user_firstname,
                        u.lastname as user_lastname,
                        u.email as user_email,
                        u.role as user_role
                    FROM collection c
                    JOIN redactor_group redactor_u 
                      ON redactor_u.collection_id = c.id
                    JOIN "user" u
                      ON u.id = c.author_id
                    WHERE redactor_u.redactor_id = :id;
                """),{
                    "id": id
                    }
            )).all()

        collections = CollectionConverter.row_to_collection_short_list(collections=coll_row)
        collections = sorted(collections, key=lambda x: x.created_at, reverse=True)
        return collections
