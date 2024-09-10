import pytest
import time
import pytz
import json

from datetime import datetime
from sqlalchemy import text
from typing import List

from src.archive.repository.document import DocumentRepository
from src.archive.domains.document import Document
from src.archive.database.tables import mapper_registry
from src.archive.repository.document.statements import insert_document, insert_search_data


@pytest.fixture
def init_document(init_search_data):
    return Document(
        file_urls=["test_url_1.pdf", "test_url_2.pdf"],
        author="author",
        dating="2020",
        place_of_creating="almaty",
        variety="variety",
        addressee="addressee",
        brief_content="brief content",
        case_prod_number="case prod number",
        main_text="main text",
        search_data=init_search_data,
    )

def upload_document(id: int, upload_search_data):
    return Document(
        id=id,
        file_urls=["test_url_1.pdf", "test_url_2.pdf"],
        author="author",
        dating="2020",
        place_of_creating="almaty",
        variety="varietry",
        addressee="addressee",
        brief_content="brief content",
        case_prod_number="case prod number",
        main_text="main text",
        search_data=upload_search_data,
    )


async def save_document(
    engine,
    file_urls: List[str],
    author: str,
    dating: str,
    place_of_creating: str,
    variety: str,
    addressee: str,
    brief_content: str,
    case_prod_number: str,
    main_text: str,
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

        document_id = await conn.execute(
            insert_document,
            {
                "search_data_id": search_data_id,
                "file_urls": json.dumps(file_urls),
                "author": author,
                "dating": dating,
                "place_of_creating": place_of_creating,
                "variety": variety,
                "addressee": addressee,
                "brief_content": brief_content,
                "case_prod_number": case_prod_number,
                "main_text": main_text,
                "created_at": datetime.now(pytz.UTC)
            }
        )

        document_id = document_id.scalars().first()

        return search_data_id, document_id


class TestDocumentRepository:

    @pytest.mark.asyncio
    async def test_add_document(
        self,
        init_engine,
        get_session,
        init_document
    ):
        engine = init_engine
        session = get_session
        repository = DocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        document_model = await repository.add(init_document)
        await session.commit()

        assert document_model.id == 1

        assert document_model.search_data.id is 1

        async with engine.begin() as conn:
            document = (await conn.execute(
                text("""
                select *
                from documents
                where id=:id
                """),
                {
                    "id": document_model.id
                }
            )).one()

            assert document.file_urls == ["test_url_1.pdf", "test_url_2.pdf"]
            assert document.author == "author"
            assert document.dating == "2020"
            assert document.place_of_creating == "almaty"
            assert document.variety == "variety"
            assert document.addressee == "addressee"
            assert document.brief_content == "brief content"
            assert document.case_prod_number == "case prod number"
            assert document.main_text == "main text"
            assert document.created_at == document_model.created_at
            assert document.search_data_id == document_model.search_data.id

            search_data = (await conn.execute(
                text("""
                    select * from search_data where id=:id
                """),
                {
                    "id": document_model.search_data.id
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
    async def test_add_two_documents(
        self,
        init_engine,
        get_session,
        init_document
    ):
        engine = init_engine
        session = get_session
        repository = DocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        search_data_id, document_id = await save_document(
            engine=engine,
            file_urls = ["test_url_1.pdf", "test_url_2.pdf"],
            author = "author",
            dating = "dating",
            place_of_creating = "place of creating",
            variety = "variety",
            addressee = "addressee",
            brief_content = "brief content",
            case_prod_number = "case prod number",
            main_text = "main text",
            search_data_cypher = "cypher",
            search_data_fund = "fund",
            search_data_inventory = "inventory",
            search_data_case = "case",
            search_data_leaf = "leaf",
            search_data_authenticity = "authenticity",
            search_data_lang = "lang",
            search_data_playback_method = "playback method",
            search_data_other = "other"
        )


        document_model = await repository.add(init_document)
        await session.commit()
        assert document_id == 1
        assert search_data_id == 1
        assert document_model.id == 2
        assert document_model.search_data.id == 2

        async with engine.begin() as conn:
            document = (await conn.execute(
                text("""
                select *
                from documents
                where id=:id
                """),
                {
                    "id": document_model.id
                }
            )).one()

            assert document.file_urls == ["test_url_1.pdf", "test_url_2.pdf"]
            assert document.author == "author"
            assert document.dating == "2020"
            assert document.place_of_creating == "almaty"
            assert document.variety == "variety"
            assert document.addressee == "addressee"
            assert document.brief_content == "brief content"
            assert document.case_prod_number == "case prod number"
            assert document.main_text == "main text"
            assert document.created_at == document_model.created_at
            assert document.search_data_id == document_model.search_data.id

            search_data = (await conn.execute(
                text("""
                    select * from search_data where id=:id
                """),
                {
                    "id": document_model.search_data.id
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
    async def test_get_document(
        self,
        init_engine,
        get_session,
        init_document
    ):
        
        engine = init_engine
        session = get_session
        repository = DocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        search_data_id, document_id = await save_document(
            engine=engine,
            file_urls = ["test_url_1.pdf", "test_url_2.pdf"],
            author = "author",
            dating = "dating",
            place_of_creating = "place of creating",
            variety = "variety",
            addressee = "addressee",
            brief_content = "brief content",
            case_prod_number = "case prod number",
            main_text = "main text",
            search_data_cypher = "cypher",
            search_data_fund = "fund",
            search_data_inventory = "inventory",
            search_data_case = "case",
            search_data_leaf = "leaf",
            search_data_authenticity = "authenticity",
            search_data_lang = "lang",
            search_data_playback_method = "playback method",
            search_data_other = "other"
        )

        document = await repository.get(id=document_id)
        await session.commit()

        assert document.id == 1
        assert document.file_urls == ["test_url_1.pdf", "test_url_2.pdf"]
        assert document.author == "author"
        assert document.dating == "dating"
        assert document.place_of_creating == "place of creating"
        assert document.variety == "variety"
        assert document.addressee == "addressee"
        assert document.brief_content == "brief content"
        assert document.case_prod_number == "case prod number"
        assert document.main_text == "main text"
        assert document.search_data.id == 1
        assert document.search_data.cypher == "cypher"
        assert document.search_data.fund == "fund"
        assert document.search_data.inventory == "inventory"
        assert document.search_data.case == "case"
        assert document.search_data.leaf == "leaf"
        assert document.search_data.authenticity == "authenticity"
        assert document.search_data.lang == "lang"
        assert document.search_data.playback_method == "playback method"
        assert document.search_data.other == "other"

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
        
        await engine.dispose()


    @pytest.mark.asyncio
    async def test_get_list_document(
        self,
        init_engine,
        get_session,
        init_document
    ):
        
        engine = init_engine
        session = get_session
        repository = DocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        search_data_id, document_id = await save_document(
            engine=engine,
            file_urls = ["test_url_1.pdf", "test_url_2.pdf"],
            author = "author",
            dating = "dating",
            place_of_creating = "place of creating",
            variety = "variety",
            addressee = "addressee",
            brief_content = "brief content",
            case_prod_number = "case prod number",
            main_text = "main text",
            search_data_cypher = "cypher",
            search_data_fund = "fund",
            search_data_inventory = "inventory",
            search_data_case = "case",
            search_data_leaf = "leaf",
            search_data_authenticity = "authenticity",
            search_data_lang = "lang",
            search_data_playback_method = "playback method",
            search_data_other = "other"
        )

        documents = await repository.get_list()
        await session.commit()
        assert len(documents) == 1

        assert documents[0].id == 1
        assert documents[0].file_urls == ["test_url_1.pdf", "test_url_2.pdf"]
        assert documents[0].author == "author"
        assert documents[0].dating == "dating"
        assert documents[0].place_of_creating == "place of creating"
        assert documents[0].variety == "variety"
        assert documents[0].addressee == "addressee"
        assert documents[0].brief_content == "brief content"
        assert documents[0].case_prod_number == "case prod number"
        assert documents[0].main_text == "main text"
        assert documents[0].search_data.id == 1
        assert documents[0].search_data.cypher == "cypher"
        assert documents[0].search_data.fund == "fund"
        assert documents[0].search_data.inventory == "inventory"
        assert documents[0].search_data.case == "case"
        assert documents[0].search_data.leaf == "leaf"
        assert documents[0].search_data.authenticity == "authenticity"
        assert documents[0].search_data.lang == "lang"
        assert documents[0].search_data.playback_method == "playback method"
        assert documents[0].search_data.other == "other"

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
        
        await engine.dispose()


    @pytest.mark.asyncio
    async def test_get_list_with_two_documents(
        self,
        init_engine,
        get_session,
        init_document
    ):
        
        engine = init_engine
        session = get_session
        repository = DocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        search_data_id, document_id = await save_document(
            engine=engine,
            file_urls = ["test_url_1.pdf", "test_url_2.pdf"],
            author = "author",
            dating = "dating",
            place_of_creating = "place of creating",
            variety = "variety",
            addressee = "addressee",
            brief_content = "brief content",
            case_prod_number = "case prod number",
            main_text = "main text",
            search_data_cypher = "cypher",
            search_data_fund = "fund",
            search_data_inventory = "inventory",
            search_data_case = "case",
            search_data_leaf = "leaf",
            search_data_authenticity = "authenticity",
            search_data_lang = "lang",
            search_data_playback_method = "playback method",
            search_data_other = "other"
        )

        search_data_id_two, document_id_two = await save_document(
            engine=engine,
            file_urls = ["two_test_url_1.pdf", "two_test_url_2.pdf"],
            author = "author two",
            dating = "dating two",
            place_of_creating = "place of creating two",
            variety = "variety two",
            addressee = "addressee two",
            brief_content = "brief content two",
            case_prod_number = "case prod number two",
            main_text = "main text two",
            search_data_cypher = "cypher two",
            search_data_fund = "fund two",
            search_data_inventory = "inventory two",
            search_data_case = "case two",
            search_data_leaf = "leaf two",
            search_data_authenticity = "authenticity two",
            search_data_lang = "lang two",
            search_data_playback_method = "playback method two",
            search_data_other = None
        )

        documents = await repository.get_list()
        await session.commit()
        assert len(documents) == 2

        assert documents[0].id == 1
        assert documents[0].file_urls == ["test_url_1.pdf", "test_url_2.pdf"]
        assert documents[0].author == "author"
        assert documents[0].dating == "dating"
        assert documents[0].place_of_creating == "place of creating"
        assert documents[0].variety == "variety"
        assert documents[0].addressee == "addressee"
        assert documents[0].brief_content == "brief content"
        assert documents[0].case_prod_number == "case prod number"
        assert documents[0].main_text == "main text"
        assert documents[0].search_data.id == 1
        assert documents[0].search_data.cypher == "cypher"
        assert documents[0].search_data.fund == "fund"
        assert documents[0].search_data.inventory == "inventory"
        assert documents[0].search_data.case == "case"
        assert documents[0].search_data.leaf == "leaf"
        assert documents[0].search_data.authenticity == "authenticity"
        assert documents[0].search_data.lang == "lang"
        assert documents[0].search_data.playback_method == "playback method"
        assert documents[0].search_data.other == "other"

        assert documents[1].id == 2
        assert documents[1].file_urls == ["two_test_url_1.pdf", "two_test_url_2.pdf"]
        assert documents[1].author == "author two"
        assert documents[1].dating == "dating two"
        assert documents[1].place_of_creating == "place of creating two"
        assert documents[1].variety == "variety two"
        assert documents[1].addressee == "addressee two"
        assert documents[1].brief_content == "brief content two"
        assert documents[1].case_prod_number == "case prod number two"
        assert documents[1].main_text == "main text two"
        assert documents[1].search_data.id == 2
        assert documents[1].search_data.cypher == "cypher two"
        assert documents[1].search_data.fund == "fund two"
        assert documents[1].search_data.inventory == "inventory two"
        assert documents[1].search_data.case == "case two"
        assert documents[1].search_data.leaf == "leaf two"
        assert documents[1].search_data.authenticity == "authenticity two"
        assert documents[1].search_data.lang == "lang two"
        assert documents[1].search_data.playback_method == "playback method two"
        assert documents[1].search_data.other is None

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
        
        await engine.dispose()

    
    @pytest.mark.asyncio
    async def test_update_document(
        self,
        init_engine,
        get_session,
        upload_search_data
    ):
        
        engine = init_engine
        session = get_session
        repository = DocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        search_data_id, document_id = await save_document(
            engine=engine,
            file_urls = ["test_url_1.pdf", "test_url_2.pdf"],
            author = "author",
            dating = "dating",
            place_of_creating = "almaty",
            variety = "variety",
            addressee = "addressee",
            brief_content = "brief content",
            case_prod_number = "case prod number",
            main_text = "main text",
            search_data_cypher = "cypher",
            search_data_fund = "fund",
            search_data_inventory = "inventory",
            search_data_case = "case",
            search_data_leaf = "leaf",
            search_data_authenticity = "authenticity",
            search_data_lang = "lang",
            search_data_playback_method = "playback method",
            search_data_other = "other"
        )

        document = upload_document(id=document_id, upload_search_data=upload_search_data)
        document.search_data.update(
            new_cypher="new cypher",
            new_inventory="new inventory",
            new_leaf="new leaf",
            new_lang="new lang"
        )
        document.update(
            new_file_urls = ["new_test_url_1.pdf"],
            new_dating = "new_dating",
            new_variety = "new variety",
            new_brief_content = "new brief content",
            new_main_text = "new main text"
        )

        document = await repository.update(model=document)
        await session.commit()

        assert document.id == 1
        assert document.file_urls == ["new_test_url_1.pdf"]
        assert document.author == "author"
        assert document.dating == "new_dating"
        assert document.place_of_creating == "almaty"
        assert document.variety == "new variety"
        assert document.addressee == "addressee"
        assert document.brief_content == "new brief content"
        assert document.case_prod_number == "case prod number"
        assert document.main_text == "new main text"
        assert document.search_data.id == 1
        assert document.search_data.cypher == "new cypher"
        assert document.search_data.fund == "fund"
        assert document.search_data.inventory == "new inventory"
        assert document.search_data.case == "case"
        assert document.search_data.leaf == "new leaf"
        assert document.search_data.authenticity == "authenticity"
        assert document.search_data.lang == "new lang"
        assert document.search_data.playback_method == "playback method"
        assert document.search_data.other == "other"

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
        
        await engine.dispose()

    
    @pytest.mark.asyncio
    async def test_delete_document(
        self,
        init_engine,
        get_session,
        upload_search_data
    ):
        
        engine = init_engine
        session = get_session
        repository = DocumentRepository(session=session)

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)
            await conn.run_sync(mapper_registry.metadata.create_all)

        search_data_id, document_id = await save_document(
            engine=engine,
            file_urls = ["test_url_1.pdf", "test_url_2.pdf"],
            author = "author",
            dating = "dating",
            place_of_creating = "almaty",
            variety = "variety",
            addressee = "addressee",
            brief_content = "brief content",
            case_prod_number = "case prod number",
            main_text = "main text",
            search_data_cypher = "cypher",
            search_data_fund = "fund",
            search_data_inventory = "inventory",
            search_data_case = "case",
            search_data_leaf = "leaf",
            search_data_authenticity = "authenticity",
            search_data_lang = "lang",
            search_data_playback_method = "playback method",
            search_data_other = "other"
        )

        async with engine.begin() as conn:
            docuemnts = (await conn.execute(
                text("""
                    select * from documents
                """)
            )).all()
        assert len(docuemnts) == 1

        async with engine.begin() as conn:
            search_data_s = (await conn.execute(
                text("""
                    select * from search_data
                """)
            )).all()
        assert len(search_data_s) == 1

        await repository.delete(search_data_id=1)
        await session.commit()

        async with engine.begin() as conn:
            docuemnts = (await conn.execute(
                text("""
                    select * from documents
                """)
            )).all()
        assert len(docuemnts) == 0

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


    
