import pytest
import pytz
import json

from datetime import datetime
from sqlalchemy import text
from typing import List

from src.archive.repository.document import VideoDocumentRepository
from src.archive.domains.document import VideoDocument
from src.archive.database.tables import mapper_registry
from src.archive.repository.document.statements import insert_video_document, insert_search_data


@pytest.fixture
def init_video_document(init_search_data):
    return VideoDocument(
        file_urls=["test_url_1.mp4", "test_url_2.mp4"],
        author="author",
        dating="2020",
        place_of_creating="almaty",
        title="video title",
        volume="volume 1",
        num_of_parts="3",
        color="color",
        creator="creator",
        info_of_publication="info of publication",
        search_data=init_search_data,
    )

def upload_video_document(id: int, upload_search_data):
    return VideoDocument(
        id=id,
        file_urls=["test_url_1.mp4", "test_url_2.mp4"],
        author="author",
        dating="2020",
        place_of_creating="almaty",
        title="video title",
        volume="volume 1",
        num_of_parts="3",
        color="color",
        creator="creator",
        info_of_publication="info of publication",
        search_data=upload_search_data,
    )


async def save_video_document(
    engine,
    file_urls: List[str],
    author: str,
    dating: str,
    place_of_creating: str,
    title: str,
    volume: str,
    num_of_parts: str,
    color: str,
    creator: str,
    info_of_publication: str,
    search_data_cypher: str,
    search_data_fund: str,
    search_data_inventory: str,
    search_data_case: str,
    search_data_leaf: str,
    search_data_authenticity: str,
    search_data_lang: str,
    search_data_playback_method: str,
    search_data_other: str
):
    async with engine.begin() as conn:
        search_data_id = await conn.execute(
            insert_search_data,
            {
                "search_data_cypher": search_data_cypher,
                "search_data_fund": search_data_fund,
                "search_data_inventory": search_data_inventory,
                "search_data_case": search_data_case,
                "search_data_leaf": search_data_leaf,
                "search_data_authenticity": search_data_authenticity,
                "search_data_lang": search_data_lang,
                "search_data_playback_method": search_data_playback_method,
                "search_data_other": search_data_other
            }
        )

        search_data_id = search_data_id.scalars().first()

        video_document_id = await conn.execute(
            insert_video_document,
            {
                "search_data_id": search_data_id,
                "file_urls": json.dumps(file_urls),
                "author": author,
                "dating": dating,
                "place_of_creating": place_of_creating,
                "title": title,
                "volume": volume,
                "num_of_parts": num_of_parts,
                "color": color,
                "creator": creator,
                "info_of_publication": info_of_publication,
                "created_at": datetime.now(pytz.UTC)
            }
        )

        video_document_id = video_document_id.scalars().first()

        return search_data_id, video_document_id


class TestVideoDocumentRepository:
    @pytest.mark.asyncio
    async def test_add_video_document(
        self,
        init_engine,
        get_session,
        init_video_document
    ):
        engine = init_engine
        session = get_session
        repository = VideoDocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        video_document_model = await repository.add(init_video_document)
        await session.commit()

        assert video_document_model.id == 1

        async with engine.begin() as conn:
            video_document = (await conn.execute(
                text("""
                select *
                from video_documents
                where id=:id
                """),
                {
                    "id": video_document_model.id
                }
            )).one()

            assert video_document.file_urls == ["test_url_1.mp4", "test_url_2.mp4"]
            assert video_document.author == "author"
            assert video_document.dating == "2020"
            assert video_document.place_of_creating == "almaty"
            assert video_document.title == "video title"
            assert video_document.volume == "volume 1"
            assert video_document.num_of_parts == "3"
            assert video_document.color == "color"
            assert video_document.creator == "creator"
            assert video_document.info_of_publication == "info of publication"
            assert video_document.created_at == video_document_model.created_at
            assert video_document.search_data_id == video_document_model.search_data.id

            search_data = (await conn.execute(
                text("""
                    select * from search_data where id=:id
                """),
                {
                    "id": video_document_model.search_data.id
                }
            )).one()

            assert search_data.cypher == "cypher"
            assert search_data.fund == "fund"
            assert search_data.inventory == "inventory"
            assert search_data.case == "case"
            assert search_data.leaf == "leaf"
            assert search_data.authenticity == "authenticity"
            assert search_data.lang == "lang"
            assert search_data.playback_method == "playback method"
            assert search_data.other is None

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
        
        await engine.dispose()


    @pytest.mark.asyncio
    async def test_get_video_document(
        self,
        init_engine,
        get_session,
        init_video_document
    ):
        engine = init_engine
        session = get_session
        repository = VideoDocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        search_data_id, video_document_id = await save_video_document(
            engine=engine,
            file_urls=["test_url_1.mp4", "test_url_2.mp4"],
            author="author",
            dating="dating",
            place_of_creating="place of creating",
            title="video title",
            volume="volume 1",
            num_of_parts="3",
            color="color",
            creator="creator",
            info_of_publication="info of publication",
            search_data_cypher="cypher",
            search_data_fund="fund",
            search_data_inventory="inventory",
            search_data_case="case",
            search_data_leaf="leaf",
            search_data_authenticity="authenticity",
            search_data_lang="lang",
            search_data_playback_method="playback method",
            search_data_other="other"
        )

        video_document = await repository.get(id=video_document_id)
        await session.commit()

        assert video_document.id == 1
        assert video_document.file_urls == ["test_url_1.mp4", "test_url_2.mp4"]
        assert video_document.author == "author"
        assert video_document.dating == "dating"
        assert video_document.place_of_creating == "place of creating"
        assert video_document.title == "video title"
        assert video_document.volume == "volume 1"
        assert video_document.num_of_parts == "3"
        assert video_document.color == "color"
        assert video_document.creator == "creator"
        assert video_document.info_of_publication == "info of publication"
        assert video_document.search_data.id == 1
        assert video_document.search_data.cypher == "cypher"
        assert video_document.search_data.fund == "fund"
        assert video_document.search_data.inventory == "inventory"
        assert video_document.search_data.case == "case"
        assert video_document.search_data.leaf == "leaf"
        assert video_document.search_data.authenticity == "authenticity"
        assert video_document.search_data.lang == "lang"
        assert video_document.search_data.playback_method == "playback method"
        assert video_document.search_data.other == "other"

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
        
        await engine.dispose()

    @pytest.mark.asyncio
    async def test_get_list_with_two_video_documents(
        self,
        init_engine,
        get_session,
        init_video_document
    ):
        engine = init_engine
        session = get_session
        repository = VideoDocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        search_data_id, video_document_id = await save_video_document(
            engine=engine,
            file_urls=["test_url_1.mp4", "test_url_2.mp4"],
            author="author",
            dating="dating",
            place_of_creating="place of creating",
            title="video title",
            volume="volume 1",
            num_of_parts="3",
            color="color",
            creator="creator",
            info_of_publication="info of publication",
            search_data_cypher="cypher",
            search_data_fund="fund",
            search_data_inventory="inventory",
            search_data_case="case",
            search_data_leaf="leaf",
            search_data_authenticity="authenticity",
            search_data_lang="lang",
            search_data_playback_method="playback method",
            search_data_other="other"
        )

        search_data_id_two, video_document_id_two = await save_video_document(
            engine=engine,
            file_urls=["two_test_url_1.mp4", "two_test_url_2.mp4"],
            author="author two",
            dating="dating two",
            place_of_creating="place of creating two",
            title="video title two",
            volume="volume 2",
            num_of_parts="5",
            color="color two",
            creator="creator two",
            info_of_publication="info of publication two",
            search_data_cypher="cypher two",
            search_data_fund="fund two",
            search_data_inventory="inventory two",
            search_data_case="case two",
            search_data_leaf="leaf two",
            search_data_authenticity="authenticity two",
            search_data_lang="lang two",
            search_data_playback_method="playback method two",
            search_data_other=None
        )

        video_documents = await repository.get_list()
        await session.commit()
        assert len(video_documents) == 2

        assert video_documents[0].id == 1
        assert video_documents[0].file_urls == ["test_url_1.mp4", "test_url_2.mp4"]
        assert video_documents[0].author == "author"
        assert video_documents[0].dating == "dating"
        assert video_documents[0].place_of_creating == "place of creating"
        assert video_documents[0].title == "video title"
        assert video_documents[0].volume == "volume 1"
        assert video_documents[0].num_of_parts == "3"
        assert video_documents[0].color == "color"
        assert video_documents[0].creator == "creator"
        assert video_documents[0].info_of_publication == "info of publication"
        assert video_documents[0].search_data.id == 1
        assert video_documents[0].search_data.cypher == "cypher"
        assert video_documents[0].search_data.fund == "fund"
        assert video_documents[0].search_data.inventory == "inventory"
        assert video_documents[0].search_data.case == "case"
        assert video_documents[0].search_data.leaf == "leaf"
        assert video_documents[0].search_data.authenticity == "authenticity"
        assert video_documents[0].search_data.lang == "lang"
        assert video_documents[0].search_data.playback_method == "playback method"
        assert video_documents[0].search_data.other == "other"

        assert video_documents[1].id == 2
        assert video_documents[1].file_urls == ["two_test_url_1.mp4", "two_test_url_2.mp4"]
        assert video_documents[1].author == "author two"
        assert video_documents[1].dating == "dating two"
        assert video_documents[1].place_of_creating == "place of creating two"
        assert video_documents[1].title == "video title two"
        assert video_documents[1].volume == "volume 2"
        assert video_documents[1].num_of_parts == "5"
        assert video_documents[1].color == "color two"
        assert video_documents[1].creator == "creator two"
        assert video_documents[1].info_of_publication == "info of publication two"
        assert video_documents[1].search_data.id == 2
        assert video_documents[1].search_data.cypher == "cypher two"
        assert video_documents[1].search_data.fund == "fund two"
        assert video_documents[1].search_data.inventory == "inventory two"
        assert video_documents[1].search_data.case == "case two"
        assert video_documents[1].search_data.leaf == "leaf two"
        assert video_documents[1].search_data.authenticity == "authenticity two"
        assert video_documents[1].search_data.lang == "lang two"
        assert video_documents[1].search_data.playback_method == "playback method two"
        assert video_documents[1].search_data.other is None

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
        
        await engine.dispose()

    @pytest.mark.asyncio
    async def test_update_video_document(
        self,
        init_engine,
        get_session,
        upload_search_data
    ):
        engine = init_engine
        session = get_session
        repository = VideoDocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        search_data_id, video_document_id = await save_video_document(
            engine=engine,
            file_urls=["test_url_1.mp4", "test_url_2.mp4"],
            author="author",
            dating="dating",
            place_of_creating="almaty",
            title="video title",
            volume="volume 1",
            num_of_parts="3",
            color="color",
            creator="creator",
            info_of_publication="info of publication",
            search_data_cypher="cypher",
            search_data_fund="fund",
            search_data_inventory="inventory",
            search_data_case="case",
            search_data_leaf="leaf",
            search_data_authenticity="authenticity",
            search_data_lang="lang",
            search_data_playback_method="playback method",
            search_data_other="other"
        )

        video_document = upload_video_document(id=video_document_id, upload_search_data=upload_search_data)
        video_document.search_data.update(
            new_cypher="new cypher",
            new_inventory="new inventory",
            new_leaf="new leaf",
            new_lang="new lang"
        )
        video_document.update(
            new_file_urls=["new_test_url_1.mp4"],
            new_dating="new_dating",
            new_title="new video title",
            new_volume="new volume",
            new_num_of_parts="new num_of_parts",
            new_color="new color",
            new_creator="new creator",
            new_info_of_publication="new info of publication"
        )

        video_document = await repository.update(model=video_document)
        await session.commit()

        assert video_document.id == 1
        assert video_document.file_urls == ["new_test_url_1.mp4"]
        assert video_document.author == "author"
        assert video_document.dating == "new_dating"
        assert video_document.place_of_creating == "almaty"
        assert video_document.title == "new video title"
        assert video_document.volume == "new volume"
        assert video_document.num_of_parts == "new num_of_parts"
        assert video_document.color == "new color"
        assert video_document.creator == "new creator"
        assert video_document.info_of_publication == "new info of publication"
        assert video_document.search_data.id == 1
        assert video_document.search_data.cypher == "new cypher"
        assert video_document.search_data.fund == "fund"
        assert video_document.search_data.inventory == "new inventory"
        assert video_document.search_data.case == "case"
        assert video_document.search_data.leaf == "new leaf"
        assert video_document.search_data.authenticity == "authenticity"
        assert video_document.search_data.lang == "new lang"
        assert video_document.search_data.playback_method == "playback method"
        assert video_document.search_data.other == "other"

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
        
        await engine.dispose()

    @pytest.mark.asyncio
    async def test_delete_video_document(
        self,
        init_engine,
        get_session,
        upload_search_data
    ):
        engine = init_engine
        session = get_session
        repository = VideoDocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        search_data_id, video_document_id = await save_video_document(
            engine=engine,
            file_urls=["test_url_1.mp4", "test_url_2.mp4"],
            author="author",
            dating="dating",
            place_of_creating="almaty",
            title="video title",
            volume="volume 1",
            num_of_parts="3",
            color="color",
            creator="creator",
            info_of_publication="info of publication",
            search_data_cypher="cypher",
            search_data_fund="fund",
            search_data_inventory="inventory",
            search_data_case="case",
            search_data_leaf="leaf",
            search_data_authenticity="authenticity",
            search_data_lang="lang",
            search_data_playback_method="playback method",
            search_data_other="other"
        )

        async with engine.begin() as conn:
            video_documents = (await conn.execute(
                text("""
                    select * from video_documents
                """)
            )).all()
        assert len(video_documents) == 1

        async with engine.begin() as conn:
            search_data_s = (await conn.execute(
                text("""
                    select * from search_data
                """)
            )).all()
        assert len(search_data_s) == 1

        await repository.delete(search_data_id=search_data_id)
        await session.commit()

        async with engine.begin() as conn:
            video_documents = (await conn.execute(
                text("""
                    select * from video_documents
                """)
            )).all()
        assert len(video_documents) == 0

        async with engine.begin() as conn:
            search_data_s = (await conn.execute(
                text("""
                    select * from search_data
                """)
            )).all()
        assert len(search_data_s) == 0

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
        
        await engine.dispose()

