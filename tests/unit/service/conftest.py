import pytest

from unittest.mock import Mock

from src.archive.core import AbstractBaseEntity, AbstractRepository, AbstractUnitOfWork
from src.archive.domains.document import Document, SearchData, PhonoDocument


@pytest.fixture
def init_search_data():
    return SearchData(
        cypher="cypher",
        fund="fund",
        inventory="inventory",
        case="case",
        leaf="leaf",
        authenticity="authenticity",
        lang="lang",
        playback_method="playback method"
    )

@pytest.fixture
def init_search_data_mock():
    data = Mock()
    data.cypher = "cypher"
    data.fund = "fund"
    data.inventory = "inventory"
    data.case = "case"
    data.leaf = "leaf"
    data.authenticity = "authenticity"
    data.lang = "lang"
    data.playback_method = "playback method"
    data.other = None

    return data

@pytest.fixture
def upload_search_data():
    return SearchData(
        id=1,
        cypher="cypher",
        fund="fund",
        inventory="inventory",
        case="case",
        leaf="leaf",
        authenticity="authenticity",
        lang="lang",
        playback_method="playback method",
        other="other"
    )

@pytest.fixture
def upload_search_data_mock():
    data = Mock()
    data.id = 1
    data.cypher = "cypher"
    data.fund = "fund"
    data.inventory = "inventory"
    data.case = "case"
    data.leaf = "leaf"
    data.authenticity = "authenticity"
    data.lang=  "lang"
    data.playback_method = "playback method"
    data.other = "other"

    return data

def init_document(init_search_data):
    return Document(
        file_urls=["file_url_1.pdf", "file_url_2.pdf"],
        author="author",
        dating="2020",
        place_of_creating="almaty",
        variety="varietry",
        addressee="addressee",
        brief_content="brief content",
        case_prod_number="case prod number",
        main_text="main text",
        search_data=init_search_data(),
    )

def upload_document(id: int, upload_search_data):
    return Document(
        id=id,
        file_urls=["file_url_1.pdf", "file_url_2.pdf"],
        author="author",
        dating="2020",
        place_of_creating="almaty",
        variety="varietry",
        addressee="addressee",
        brief_content="brief content",
        case_prod_number="case prod number",
        main_text="main text",
        search_data=upload_search_data(),
    )


@pytest.fixture
def fake_document_repository_class(upload_search_data):
    class FakeDocumentRepository(AbstractRepository):
        async def add(self, model: Document):
            return Document(
                id=1,
                file_urls=model.file_urls,
                author=model.author,
                dating=model.dating,
                place_of_creating=model.place_of_creating,
                variety=model.variety,
                addressee=model.addressee,
                brief_content=model.brief_content,
                case_prod_number=model.case_prod_number,
                main_text=model.main_text,
                search_data=SearchData(
                    id=1,
                    cypher=model.search_data.cypher,
                    fund=model.search_data.fund,
                    inventory=model.search_data.inventory,
                    case=model.search_data.case,
                    leaf=model.search_data.leaf,
                    authenticity=model.search_data.authenticity,
                    lang=model.search_data.lang,
                    playback_method=model.search_data.playback_method,
                    other=model.search_data.other
                ),
                created_at=model.created_at
            )
        
        async def get(self, id: int) -> Document:
            return Document(
                id=id,
                file_urls=["file_url_1.pdf", "file_url_2.pdf"],
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
        
        async def get_list(self) -> list[Document]:
            pass

        async def update(self, model: Document):
            return Document(
                id=model.id,
                file_urls=model.file_urls,
                author=model.author,
                dating=model.dating,
                place_of_creating=model.place_of_creating,
                variety=model.variety,
                addressee=model.addressee,
                brief_content=model.brief_content,
                case_prod_number=model.case_prod_number,
                main_text=model.main_text,
                search_data=model.search_data,
                created_at=model.created_at
            )

        async def delete(self, id: int):
            pass

    return FakeDocumentRepository


@pytest.fixture
def fake_phonodocument_repository_class():
    class FakePhonoDocumentRepository(AbstractRepository):
        async def add(self, model: PhonoDocument):
            return PhonoDocument(
                id=1,
                file_urls=model.file_urls,
                author=model.author,
                dating=model.dating,
                place_of_creating=model.place_of_creating,
                genre=model.genre,
                brief_summary=model.brief_summary,
                addressee=model.addressee,
                cypher=model.cypher,
                lang=model.lang,
                storage_media=model.storage_media,
                created_at=model.created_at
            )
        
        async def get(self, id: int) -> PhonoDocument:
            return PhonoDocument(
                id=id,
                file_urls=["file_url_1.mp3", "file_url_2.mp3"],
                author="author",
                dating="2020",
                place_of_creating="almaty",
                genre="genre",
                brief_summary="brief summary",
                addressee="addressee",
                cypher="cypher",
                lang="lang",
                storage_media="storage media",
            )
        
        async def get_list(self) -> list[PhonoDocument]:
            pass

        async def update(self, model: PhonoDocument):
            return PhonoDocument(
                id=model.id,
                file_urls=model.file_urls,
                author=model.author,
                dating=model.dating,
                place_of_creating=model.place_of_creating,
                genre=model.genre,
                brief_summary=model.brief_summary,
                addressee=model.addressee,
                cypher=model.cypher,
                lang=model.lang,
                storage_media=model.storage_media,
                created_at=model.created_at
            )

        async def delete(self, id: int):
            pass

    return FakePhonoDocumentRepository


@pytest.fixture
def fake_unit_of_work():
    class FakeUnitOfWork(AbstractUnitOfWork):
        def __init__(self, repository: AbstractRepository) -> None:
            self.repository = repository

        async def __aenter__(self):
            self.repository = self.repository()
            return await super().__aenter__()
        
        async def __aexit__(self, *args):
            await super().__aexit__()

        async def commit(self):
            pass

        async def rollback(self):
            pass

    return FakeUnitOfWork
