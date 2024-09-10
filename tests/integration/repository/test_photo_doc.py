import pytest
import pytz
import json

from datetime import datetime
from sqlalchemy import text
from typing import List

from src.archive.repository.document import PhotoDocumentRepository
from src.archive.domains.document import PhotoDocument
from src.archive.database.tables import mapper_registry
from src.archive.repository.document.statements import insert_photo_document, insert_search_data


@pytest.fixture
def init_photo_document(init_search_data):
    return PhotoDocument(
        file_urls=["test_url_1.jpg", "test_url_2.jpg"],
        author="author",
        dating="2020",
        place_of_creating="almaty",
        title="photo title",
        completeness_of_reproduction="complete",
        storage_media="digital",
        color="color",
        size_of_original="10x15",
        image_scale="1:1",
        search_data=init_search_data,
    )

def upload_photo_document(id: int, upload_search_data):
    return PhotoDocument(
        id=id,
        file_urls=["test_url_1.jpg", "test_url_2.jpg"],
        author="author",
        dating="2020",
        place_of_creating="almaty",
        title="photo title",
        completeness_of_reproduction="complete",
        storage_media="digital",
        color="color",
        size_of_original="10x15",
        image_scale="1:1",
        search_data=upload_search_data,
    )

async def save_photo_document(
    engine,
    file_urls: List[str],
    author: str,
    dating: str,
    place_of_creating: str,
    title: str,
    completeness_of_reproduction: str,
    storage_media: str,
    color: str,
    size_of_original: str,
    image_scale: str,
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

        photo_document_id = await conn.execute(
            insert_photo_document,
            {
                "search_data_id": search_data_id,
                "file_urls": json.dumps(file_urls),
                "author": author,
                "dating": dating,
                "place_of_creating": place_of_creating,
                "title": title,
                "completeness_of_reproduction": completeness_of_reproduction,
                "storage_media": storage_media,
                "color": color,
                "size_of_original": size_of_original,
                "image_scale": image_scale,
                "created_at": datetime.now(pytz.UTC)
            }
        )

        photo_document_id = photo_document_id.scalars().first()

        return search_data_id, photo_document_id


class TestPhotoDocumentRepository:

    @pytest.mark.asyncio
    async def test_add_photo_document(
        self,
        init_engine,
        get_session,
        init_photo_document
    ):
        engine = init_engine
        session = get_session
        repository = PhotoDocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        photo_document_model = await repository.add(init_photo_document)
        await session.commit()

        assert photo_document_model.id == 1

        async with engine.begin() as conn:
            photo_document = (await conn.execute(
                text("""
                select *
                from photo_documents
                where id=:id
                """),
                {
                    "id": photo_document_model.id
                }
            )).one()

            assert photo_document.file_urls == ["test_url_1.jpg", "test_url_2.jpg"]
            assert photo_document.author == "author"
            assert photo_document.dating == "2020"
            assert photo_document.place_of_creating == "almaty"
            assert photo_document.title == "photo title"
            assert photo_document.completeness_of_reproduction == "complete"
            assert photo_document.storage_media == "digital"
            assert photo_document.color == "color"
            assert photo_document.size_of_original == "10x15"
            assert photo_document.image_scale == "1:1"
            assert photo_document.created_at == photo_document_model.created_at
            assert photo_document.search_data_id == photo_document_model.search_data.id

            search_data = (await conn.execute(
                text("""
                    select * from search_data where id=:id
                """),
                {
                    "id": photo_document_model.search_data.id
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
    async def test_get_photo_document(
        self,
        init_engine,
        get_session,
        init_photo_document
    ):
        engine = init_engine
        session = get_session
        repository = PhotoDocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        search_data_id, photo_document_id = await save_photo_document(
            engine=engine,
            file_urls=["test_url_1.jpg", "test_url_2.jpg"],
            author="author",
            dating="dating",
            place_of_creating="place of creating",
            title="photo title",
            completeness_of_reproduction="complete",
            storage_media="digital",
            color="color",
            size_of_original="10x15",
            image_scale="1:1",
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

        photo_document = await repository.get(id=photo_document_id)
        await session.commit()

        assert photo_document.id == 1
        assert photo_document.file_urls == ["test_url_1.jpg", "test_url_2.jpg"]
        assert photo_document.author == "author"
        assert photo_document.dating == "dating"
        assert photo_document.place_of_creating == "place of creating"
        assert photo_document.title == "photo title"
        assert photo_document.completeness_of_reproduction == "complete"
        assert photo_document.storage_media == "digital"
        assert photo_document.color == "color"
        assert photo_document.size_of_original == "10x15"
        assert photo_document.image_scale == "1:1"
        assert photo_document.search_data.id == 1
        assert photo_document.search_data.cypher == "cypher"
        assert photo_document.search_data.fund == "fund"
        assert photo_document.search_data.inventory == "inventory"
        assert photo_document.search_data.case == "case"
        assert photo_document.search_data.leaf == "leaf"
        assert photo_document.search_data.authenticity == "authenticity"
        assert photo_document.search_data.lang == "lang"
        assert photo_document.search_data.playback_method == "playback method"
        assert photo_document.search_data.other == "other"

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
        
        await engine.dispose()

    @pytest.mark.asyncio
    async def test_get_list_photo_document(
        self,
        init_engine,
        get_session,
        init_photo_document
    ):
        engine = init_engine
        session = get_session
        repository = PhotoDocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        search_data_id, photo_document_id = await save_photo_document(
            engine=engine,
            file_urls=["test_url_1.jpg", "test_url_2.jpg"],
            author="author",
            dating="dating",
            place_of_creating="place of creating",
            title="photo title",
            completeness_of_reproduction="complete",
            storage_media="digital",
            color="color",
            size_of_original="10x15",
            image_scale="1:1",
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

        photo_documents = await repository.get_list()
        await session.commit()

        assert len(photo_documents) == 1

        assert photo_documents[0].id == 1
        assert photo_documents[0].file_urls == ["test_url_1.jpg", "test_url_2.jpg"]
        assert photo_documents[0].author == "author"
        assert photo_documents[0].dating == "dating"
        assert photo_documents[0].place_of_creating == "place of creating"
        assert photo_documents[0].title == "photo title"
        assert photo_documents[0].completeness_of_reproduction == "complete"
        assert photo_documents[0].storage_media == "digital"
        assert photo_documents[0].color == "color"
        assert photo_documents[0].size_of_original == "10x15"
        assert photo_documents[0].image_scale == "1:1"
        assert photo_documents[0].search_data.id == 1
        assert photo_documents[0].search_data.cypher == "cypher"
        assert photo_documents[0].search_data.fund == "fund"
        assert photo_documents[0].search_data.inventory == "inventory"
        assert photo_documents[0].search_data.case == "case"
        assert photo_documents[0].search_data.leaf == "leaf"
        assert photo_documents[0].search_data.authenticity == "authenticity"
        assert photo_documents[0].search_data.lang == "lang"
        assert photo_documents[0].search_data.playback_method == "playback method"
        assert photo_documents[0].search_data.other == "other"

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
        
        await engine.dispose()

    @pytest.mark.asyncio
    async def test_get_list_with_two_photo_documents(
        self,
        init_engine,
        get_session,
        init_photo_document
    ):
        engine = init_engine
        session = get_session
        repository = PhotoDocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        search_data_id, photo_document_id = await save_photo_document(
            engine=engine,
            file_urls=["test_url_1.jpg", "test_url_2.jpg"],
            author="author",
            dating="dating",
            place_of_creating="place of creating",
            title="photo title",
            completeness_of_reproduction="complete",
            storage_media="digital",
            color="color",
            size_of_original="10x15",
            image_scale="1:1",
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

        search_data_id_two, photo_document_id_two = await save_photo_document(
            engine=engine,
            file_urls=["two_test_url_1.jpg", "two_test_url_2.jpg"],
            author="author two",
            dating="dating two",
            place_of_creating="place of creating two",
            title="photo title two",
            completeness_of_reproduction="complete two",
            storage_media="digital two",
            color="color two",
            size_of_original="20x30",
            image_scale="1:2",
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

        photo_documents = await repository.get_list()
        await session.commit()
        assert len(photo_documents) == 2

        assert photo_documents[0].id == 1
        assert photo_documents[0].file_urls == ["test_url_1.jpg", "test_url_2.jpg"]
        assert photo_documents[0].author == "author"
        assert photo_documents[0].dating == "dating"
        assert photo_documents[0].place_of_creating == "place of creating"
        assert photo_documents[0].title == "photo title"
        assert photo_documents[0].completeness_of_reproduction == "complete"
        assert photo_documents[0].storage_media == "digital"
        assert photo_documents[0].color == "color"
        assert photo_documents[0].size_of_original == "10x15"
        assert photo_documents[0].image_scale == "1:1"
        assert photo_documents[0].search_data.id == 1
        assert photo_documents[0].search_data.cypher == "cypher"
        assert photo_documents[0].search_data.fund == "fund"
        assert photo_documents[0].search_data.inventory == "inventory"
        assert photo_documents[0].search_data.case == "case"
        assert photo_documents[0].search_data.leaf == "leaf"
        assert photo_documents[0].search_data.authenticity == "authenticity"
        assert photo_documents[0].search_data.lang == "lang"
        assert photo_documents[0].search_data.playback_method == "playback method"
        assert photo_documents[0].search_data.other == "other"

        assert photo_documents[1].id == 2
        assert photo_documents[1].file_urls == ["two_test_url_1.jpg", "two_test_url_2.jpg"]
        assert photo_documents[1].author == "author two"
        assert photo_documents[1].dating == "dating two"
        assert photo_documents[1].place_of_creating == "place of creating two"
        assert photo_documents[1].title == "photo title two"
        assert photo_documents[1].completeness_of_reproduction == "complete two"
        assert photo_documents[1].storage_media == "digital two"
        assert photo_documents[1].color == "color two"
        assert photo_documents[1].size_of_original == "20x30"
        assert photo_documents[1].image_scale == "1:2"
        assert photo_documents[1].search_data.id == 2
        assert photo_documents[1].search_data.cypher == "cypher two"
        assert photo_documents[1].search_data.fund == "fund two"
        assert photo_documents[1].search_data.inventory == "inventory two"
        assert photo_documents[1].search_data.case == "case two"
        assert photo_documents[1].search_data.leaf == "leaf two"
        assert photo_documents[1].search_data.authenticity == "authenticity two"
        assert photo_documents[1].search_data.lang == "lang two"
        assert photo_documents[1].search_data.playback_method == "playback method two"
        assert photo_documents[1].search_data.other is None

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
        
        await engine.dispose()

    @pytest.mark.asyncio
    async def test_update_photo_document(
        self,
        init_engine,
        get_session,
        upload_search_data
    ):
        engine = init_engine
        session = get_session
        repository = PhotoDocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        search_data_id, photo_document_id = await save_photo_document(
            engine=engine,
            file_urls=["test_url_1.jpg", "test_url_2.jpg"],
            author="author",
            dating="dating",
            place_of_creating="almaty",
            title="photo title",
            completeness_of_reproduction="complete",
            storage_media="digital",
            color="color",
            size_of_original="10x15",
            image_scale="1:1",
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

        photo_document = upload_photo_document(id=photo_document_id, upload_search_data=upload_search_data)
        photo_document.search_data.update(
            new_cypher="new cypher",
            new_inventory="new inventory",
            new_leaf="new leaf",
            new_lang="new lang"
        )
        photo_document.update(
            new_file_urls=["new_test_url_1.jpg"],
            new_dating="new_dating",
            new_title="new photo title",
            new_completeness_of_reproduction="new complete",
            new_storage_media="new digital",
            new_color="new color",
            new_size_of_original="new 10x15",
            new_image_scale="new 1:1"
        )

        photo_document = await repository.update(model=photo_document)
        await session.commit()

        assert photo_document.id == 1
        assert photo_document.file_urls == ["new_test_url_1.jpg"]
        assert photo_document.author == "author"
        assert photo_document.dating == "new_dating"
        assert photo_document.place_of_creating == "almaty"
        assert photo_document.title == "new photo title"
        assert photo_document.completeness_of_reproduction == "new complete"
        assert photo_document.storage_media == "new digital"
        assert photo_document.color == "new color"
        assert photo_document.size_of_original == "new 10x15"
        assert photo_document.image_scale == "new 1:1"
        assert photo_document.search_data.id == 1
        assert photo_document.search_data.cypher == "new cypher"
        assert photo_document.search_data.fund == "fund"
        assert photo_document.search_data.inventory == "new inventory"
        assert photo_document.search_data.case == "case"
        assert photo_document.search_data.leaf == "new leaf"
        assert photo_document.search_data.authenticity == "authenticity"
        assert photo_document.search_data.lang == "new lang"
        assert photo_document.search_data.playback_method == "playback method"
        assert photo_document.search_data.other == "other"

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
        
        await engine.dispose()

    @pytest.mark.asyncio
    async def test_delete_photo_document(
        self,
        init_engine,
        get_session,
        upload_search_data
    ):
        engine = init_engine
        session = get_session
        repository = PhotoDocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        search_data_id, photo_document_id = await save_photo_document(
            engine=engine,
            file_urls=["test_url_1.jpg", "test_url_2.jpg"],
            author="author",
            dating="dating",
            place_of_creating="almaty",
            title="photo title",
            completeness_of_reproduction="complete",
            storage_media="digital",
            color="color",
            size_of_original="10x15",
            image_scale="1:1",
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
            photo_documents = (await conn.execute(
                text("""
                    select * from photo_documents
                """)
            )).all()
        assert len(photo_documents) == 1

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
            photo_documents = (await conn.execute(
                text("""
                    select * from photo_documents
                """)
            )).all()
        assert len(photo_documents) == 0

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

