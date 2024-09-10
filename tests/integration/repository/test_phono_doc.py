import pytest
import pytz
import json

from datetime import datetime
from sqlalchemy import text
from typing import List

from src.archive.repository.document import PhonoDocumentRepository
from src.archive.domains.document import PhonoDocument
from src.archive.database.tables import mapper_registry
from src.archive.repository.document.statements import insert_phono_document


@pytest.fixture
def init_phono_document():
    return PhonoDocument(
        file_urls=["test_url_1.mp3", "test_url_2.mp3"],
        author="author",
        dating="2020",
        place_of_creating="almaty",
        genre="genre",
        brief_summary="brief summary",
        addressee="addressee",
        cypher="cypher",
        lang="lang",
        storage_media="digital",
        created_at=datetime.now(pytz.UTC)
    )

def upload_phono_document(id: int):
    return PhonoDocument(
        id=id,
        file_urls=["test_url_1.mp3", "test_url_2.mp3"],
        author="author",
        dating="2020",
        place_of_creating="almaty",
        genre="genre",
        brief_summary="brief summary",
        addressee="addressee",
        cypher="cypher",
        lang="lang",
        storage_media="digital",
        created_at=datetime.now(pytz.UTC)
    )


async def save_phono_document(
    engine,
    file_urls: List[str],
    author: str,
    dating: str,
    place_of_creating: str,
    genre: str,
    brief_summary: str,
    addressee: str,
    cypher: str,
    lang: str,
    storage_media: str
):
    async with engine.begin() as conn:
        phono_document_id = await conn.execute(
            insert_phono_document,
            {
                "file_urls": json.dumps(file_urls),
                "author": author,
                "dating": dating,
                "place_of_creating": place_of_creating,
                "genre": genre,
                "brief_summary": brief_summary,
                "addressee": addressee,
                "cypher": cypher,
                "lang": lang,
                "storage_media": storage_media,
                "created_at": datetime.now(pytz.UTC)
            }
        )

        phono_document_id = phono_document_id.scalars().first()

        return phono_document_id


class TestPhonoDocumentRepository:
    @pytest.mark.asyncio
    async def test_add_phono_document(
        self,
        init_engine,
        get_session,
        init_phono_document
    ):
        engine = init_engine
        session = get_session
        repository = PhonoDocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        phono_document_model = await repository.add(init_phono_document)
        await session.commit()

        assert phono_document_model.id == 1

        async with engine.begin() as conn:
            phono_document = (await conn.execute(
                text("""
                select *
                from phono_documents
                where id=:id
                """),
                {
                    "id": phono_document_model.id
                }
            )).one()

            assert phono_document.file_urls == ["test_url_1.mp3", "test_url_2.mp3"]
            assert phono_document.author == "author"
            assert phono_document.dating == "2020"
            assert phono_document.place_of_creating == "almaty"
            assert phono_document.genre == "genre"
            assert phono_document.brief_summary == "brief summary"
            assert phono_document.addressee == "addressee"
            assert phono_document.cypher == "cypher"
            assert phono_document.lang == "lang"
            assert phono_document.storage_media == "digital"
            assert phono_document.created_at == phono_document_model.created_at

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
        
        await engine.dispose()
    
    @pytest.mark.asyncio
    async def test_get_phono_document(
        self,
        init_engine,
        get_session,
        init_phono_document
    ):
        engine = init_engine
        session = get_session
        repository = PhonoDocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        phono_document_id = await save_phono_document(
            engine=engine,
            file_urls=["test_url_1.mp3", "test_url_2.mp3"],
            author="author",
            dating="2020",
            place_of_creating="almaty",
            genre="genre",
            brief_summary="brief summary",
            addressee="addressee",
            cypher="cypher",
            lang="lang",
            storage_media="digital"
        )

        phono_document = await repository.get(id=phono_document_id)
        await session.commit()

        assert phono_document.id == 1
        assert phono_document.file_urls == ["test_url_1.mp3", "test_url_2.mp3"]
        assert phono_document.author == "author"
        assert phono_document.dating == "2020"
        assert phono_document.place_of_creating == "almaty"
        assert phono_document.genre == "genre"
        assert phono_document.brief_summary == "brief summary"
        assert phono_document.addressee == "addressee"
        assert phono_document.cypher == "cypher"
        assert phono_document.lang == "lang"
        assert phono_document.storage_media == "digital"

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
        
        await engine.dispose()

    @pytest.mark.asyncio
    async def test_get_list_with_two_phono_documents(
        self,
        init_engine,
        get_session,
        init_phono_document
    ):
        engine = init_engine
        session = get_session
        repository = PhonoDocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        phono_document_id = await save_phono_document(
            engine=engine,
            file_urls=["test_url_1.mp3", "test_url_2.mp3"],
            author="author",
            dating="2020",
            place_of_creating="almaty",
            genre="genre",
            brief_summary="brief summary",
            addressee="addressee",
            cypher="cypher",
            lang="lang",
            storage_media="digital"
        )

        phono_document_id_two = await save_phono_document(
            engine=engine,
            file_urls=["two_test_url_1.mp3", "two_test_url_2.mp3"],
            author="author two",
            dating="2022",
            place_of_creating="almaty two",
            genre="genre two",
            brief_summary="brief summary two",
            addressee="addressee two",
            cypher="cypher two",
            lang="lang two",
            storage_media="digital two"
        )

        phono_documents = await repository.get_list()
        await session.commit()
        assert len(phono_documents) == 2

        assert phono_documents[0].id == 1
        assert phono_documents[0].file_urls == ["test_url_1.mp3", "test_url_2.mp3"]
        assert phono_documents[0].author == "author"
        assert phono_documents[0].dating == "2020"
        assert phono_documents[0].place_of_creating == "almaty"
        assert phono_documents[0].genre == "genre"
        assert phono_documents[0].brief_summary == "brief summary"
        assert phono_documents[0].addressee == "addressee"
        assert phono_documents[0].cypher == "cypher"
        assert phono_documents[0].lang == "lang"
        assert phono_documents[0].storage_media == "digital"

        assert phono_documents[1].id == 2
        assert phono_documents[1].file_urls == ["two_test_url_1.mp3", "two_test_url_2.mp3"]
        assert phono_documents[1].author == "author two"
        assert phono_documents[1].dating == "2022"
        assert phono_documents[1].place_of_creating == "almaty two"
        assert phono_documents[1].genre == "genre two"
        assert phono_documents[1].brief_summary == "brief summary two"
        assert phono_documents[1].addressee == "addressee two"
        assert phono_documents[1].cypher == "cypher two"
        assert phono_documents[1].lang == "lang two"
        assert phono_documents[1].storage_media == "digital two"

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
        
        await engine.dispose()

    @pytest.mark.asyncio
    async def test_update_phono_document(
        self,
        init_engine,
        get_session
    ):
        engine = init_engine
        session = get_session
        repository = PhonoDocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        phono_document_id = await save_phono_document(
            engine=engine,
            file_urls=["test_url_1.mp3", "test_url_2.mp3"],
            author="author",
            dating="dating",
            place_of_creating="almaty",
            genre="genre",
            brief_summary="brief summary",
            addressee="addressee",
            cypher="cypher",
            lang="lang",
            storage_media="digital"
        )

        phono_document = upload_phono_document(id=phono_document_id)
        phono_document.update(
            new_file_urls=["new_test_url_1.mp3"],
            new_dating="new_dating",
            new_genre="new genre",
            new_brief_summary="new brief summary",
            new_addressee="new addressee",
            new_cypher="new cypher",
            new_lang="new lang",
            new_storage_media="new digital"
        )

        phono_document = await repository.update(model=phono_document)
        await session.commit()

        assert phono_document.id == 1
        assert phono_document.file_urls == ["new_test_url_1.mp3"]
        assert phono_document.author == "author"
        assert phono_document.dating == "new_dating"
        assert phono_document.place_of_creating == "almaty"
        assert phono_document.genre == "new genre"
        assert phono_document.brief_summary == "new brief summary"
        assert phono_document.addressee == "new addressee"
        assert phono_document.cypher == "new cypher"
        assert phono_document.lang == "new lang"
        assert phono_document.storage_media == "new digital"

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
        
        await engine.dispose()

    @pytest.mark.asyncio
    async def test_delete_phono_document(
        self,
        init_engine,
        get_session
    ):
        engine = init_engine
        session = get_session
        repository = PhonoDocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        phono_document_id = await save_phono_document(
            engine=engine,
            file_urls=["test_url_1.mp3", "test_url_2.mp3"],
            author="author",
            dating="dating",
            place_of_creating="almaty",
            genre="genre",
            brief_summary="brief summary",
            addressee="addressee",
            cypher="cypher",
            lang="lang",
            storage_media="digital"
        )

        async with engine.begin() as conn:
            phono_documents = (await conn.execute(
                text("""
                    select * from phono_documents
                """)
            )).all()
        assert len(phono_documents) == 1

        await repository.delete(id=phono_document_id)
        await session.commit()

        async with engine.begin() as conn:
            phono_documents = (await conn.execute(
                text("""
                    select * from phono_documents
                """)
            )).all()
        assert len(phono_documents) == 0

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
        
        await engine.dispose()

