import pytest

from src.archive.core import AbstractBaseEntity, AbstractRepository, AbstractUnitOfWork
from src.archive.domains.document import Document, SearchData


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

def init_document(init_search_data):
    return Document(
        file_url="test_url.pdf",
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
        file_url="test_url.pdf",
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
                file_url=model.file_url,
                author=model.author,
                dating=model.dating,
                place_of_creating=model.place_of_creating,
                variety=model.variety,
                addressee=model.addressee,
                brief_content=model.brief_content,
                case_prod_number=model.case_prod_number,
                main_text=model.main_text,
                search_data=upload_search_data,
                created_at=model.created_at
            )
        
        async def get(self, id: int) -> Document:
            return Document(
                id=id,
                file_url="test_url.pdf",
                author="author",
                dating="2020",
                place_of_creating="almaty",
                variety="varietry",
                addressee="addressee",
                brief_content="brief content",
                case_prod_number="case prod number",
                main_text="main text",
                search_data="search data",
            )
        
        async def get_list(self) -> list[Document]:
            pass

        async def update(self, id: int, model: Document):
            pass

        async def delete(self, id: int):
            pass
    return FakeDocumentRepository


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