import pytest
import os

from unittest.mock import Mock, mock_open, AsyncMock, patch
from datetime import datetime

from src.archive.domains.document import Document, SearchData
from src.archive.service.document import DocumentService


@pytest.fixture
def init_document_mock(init_search_data_mock):

    data = Mock()
    data.file_url = "test_url.pdf"
    data.author = "author"
    data.dating = "2020"
    data.place_of_creating = "almaty"
    data.variety = "variety"
    data.addressee = "addressee"
    data.brief_content = "brief content"
    data.case_prod_number = "case prod number"
    data.main_text = "main text"
    data.search_data = init_search_data_mock

    return data

@pytest.fixture
def upload_document_mock(upload_search_data_mock, id=1):
    data = Mock()
    data.id = id
    data.file_url="test_url.pdf"
    data.author="author"
    data.dating="2020"
    data.place_of_creating="almaty"
    data.variety="varietry"
    data.addressee="addressee"
    data.brief_content="brief content"
    data.case_prod_number="case prod number"
    data.main_text="main text"
    data.search_data=upload_search_data_mock

    return data


class TestUnitDocumentService:

    @pytest.mark.asyncio
    async def test_create_document(
            self,
            fake_unit_of_work,
            fake_document_repository_class,
            init_document_mock
    ):
        uow = fake_unit_of_work(repository=fake_document_repository_class)
        service = DocumentService()

        m_open = mock_open()

        with patch('builtins.open', m_open):
            document = await service.create_document(file=b'file_bytes', data=init_document_mock, uow=uow)

            assert document.id == 1
            assert isinstance(document.created_at, datetime)
            assert document.file_url == "test_url.pdf"
            assert document.author == "author"
            assert document.dating == "2020"
            assert document.place_of_creating == "almaty"
            assert document.variety == "variety"
            assert document.addressee == "addressee"
            assert document.brief_content == "brief content"
            assert document.case_prod_number == "case prod number"
            assert document.main_text == "main text"

            assert document.search_data.id is 1
            assert document.search_data.cypher == "cypher"
            assert document.search_data.fund == "fund"
            assert document.search_data.inventory == "inventory"
            assert document.search_data.case == "case"
            assert document.search_data.leaf == "leaf"
            assert document.search_data.authenticity == "authenticity"
            assert document.search_data.lang == "lang"
            assert document.search_data.playback_method == "playback method"
            assert document.search_data.other is None

            m_open.assert_called_once_with(f"files/{document.file_url}", "wb")             
            handle = m_open()
            handle.write.assert_called_once_with(b'file_bytes')

    @pytest.mark.asyncio
    async def test_update_with_file_document(
        self,
        fake_unit_of_work,
        fake_document_repository_class,
        upload_search_data_mock
    ):
        update_data = Mock()

        update_data.file_url = "new_test_url.pdf"
        update_data.author = "new author"
        update_data.dating = "new 2020"
        update_data.place_of_creating = "new almaty"
        update_data.variety = "new variety"
        update_data.addressee = "new addressee"
        update_data.brief_content = "new brief content"
        update_data.case_prod_number = "new case prod number"
        update_data.main_text = "new main text"
        update_data.search_data = upload_search_data_mock

        uow = fake_unit_of_work(repository=fake_document_repository_class)
        service = DocumentService()

        m_open = mock_open()

        with patch('builtins.open', m_open), patch('os.rename') as mock_rename:
            document = await service.update_document(id=1, file=b'new file_bytes', data=update_data, uow=uow)

            assert document.id == 1
            assert isinstance(document.created_at, datetime)
            assert document.file_url == "new_test_url.pdf"
            assert document.author == "new author"
            assert document.dating == "new 2020"
            assert document.place_of_creating == "new almaty"
            assert document.variety == "new variety"
            assert document.addressee == "new addressee"
            assert document.brief_content == "new brief content"
            assert document.case_prod_number == "new case prod number"
            assert document.main_text == "new main text"

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

            mock_rename.assert_called_once_with("files/test_url.pdf", "files/new_test_url.pdf")

            m_open.assert_called_once_with(f"files/new_test_url.pdf", "wb")             
            handle = m_open()
            handle.write.assert_called_once_with(b'new file_bytes')

    @pytest.mark.asyncio
    async def test_update_without_file_document(
        self,
        fake_unit_of_work,
        fake_document_repository_class,
        upload_search_data_mock
    ):
        update_data = Mock()

        update_data.file_url = "new_test_url.pdf"
        update_data.author = "new author"
        update_data.dating = "new 2020"
        update_data.place_of_creating = "new almaty"
        update_data.variety = "new variety"
        update_data.addressee = "new addressee"
        update_data.brief_content = "new brief content"
        update_data.case_prod_number = "new case prod number"
        update_data.main_text = "new main text"
        update_data.search_data = upload_search_data_mock

        uow = fake_unit_of_work(repository=fake_document_repository_class)
        service = DocumentService()

        m_open = mock_open()

        with patch('builtins.open', m_open), patch('os.rename') as mock_rename:
            document = await service.update_document(id=1, file=None, data=update_data, uow=uow)

            assert document.id == 1
            assert isinstance(document.created_at, datetime)
            assert document.file_url == "new_test_url.pdf"
            assert document.author == "new author"
            assert document.dating == "new 2020"
            assert document.place_of_creating == "new almaty"
            assert document.variety == "new variety"
            assert document.addressee == "new addressee"
            assert document.brief_content == "new brief content"
            assert document.case_prod_number == "new case prod number"
            assert document.main_text == "new main text"

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

            mock_rename.assert_called_once_with("files/test_url.pdf", "files/new_test_url.pdf")

            with pytest.raises(AssertionError) as error:
                m_open.assert_called_once_with(f"files/new_test_url", "wb")             
                handle = m_open()
                handle.write.assert_called_once_with(b'new file_bytes')

            assert str(error.value) == "Expected 'open' to be called once. Called 0 times."


    @pytest.mark.asyncio
    async def test_update_with_updated_search_data_document(
        self,
        fake_unit_of_work,
        fake_document_repository_class,
    ):
        update_serach_data = Mock()
        update_serach_data.id = 1
        update_serach_data.cypher = "new cypher"
        update_serach_data.fund = "new fund"
        update_serach_data.inventory = "new inventory"
        update_serach_data.case = "new case"
        update_serach_data.leaf = "new leaf"
        update_serach_data.authenticity = "new authenticity"
        update_serach_data.lang = "new lang"
        update_serach_data.playback_method = "new playback method"
        update_serach_data.other = "new other"
        update_data = Mock()

        update_data.file_url = "new_test_url.pdf"
        update_data.author = "new author"
        update_data.dating = "new 2020"
        update_data.place_of_creating = "new almaty"
        update_data.variety = "new variety"
        update_data.addressee = "new addressee"
        update_data.brief_content = "new brief content"
        update_data.case_prod_number = "new case prod number"
        update_data.main_text = "new main text"
        update_data.search_data = update_serach_data

        uow = fake_unit_of_work(repository=fake_document_repository_class)
        service = DocumentService()

        m_open = mock_open()

        with patch('builtins.open', m_open), patch('os.rename') as mock_rename:
            document = await service.update_document(id=1, file=None, data=update_data, uow=uow)

            assert document.id == 1
            assert isinstance(document.created_at, datetime)
            assert document.file_url == "new_test_url.pdf"
            assert document.author == "new author"
            assert document.dating == "new 2020"
            assert document.place_of_creating == "new almaty"
            assert document.variety == "new variety"
            assert document.addressee == "new addressee"
            assert document.brief_content == "new brief content"
            assert document.case_prod_number == "new case prod number"
            assert document.main_text == "new main text"

            assert document.search_data.id == 1
            assert document.search_data.cypher == "new cypher"
            assert document.search_data.fund == "new fund"
            assert document.search_data.inventory == "new inventory"
            assert document.search_data.case == "new case"
            assert document.search_data.leaf == "new leaf"
            assert document.search_data.authenticity == "new authenticity"
            assert document.search_data.lang == "new lang"
            assert document.search_data.playback_method == "new playback method"
            assert document.search_data.other == "new other"

            mock_rename.assert_called_once_with("files/test_url.pdf", "files/new_test_url.pdf")

            with pytest.raises(AssertionError) as error:
                m_open.assert_called_once_with(f"files/{document.file_url}", "wb")             
                handle = m_open()
                handle.write.assert_called_once_with(b'new file_bytes')

            assert str(error.value) == "Expected 'open' to be called once. Called 0 times."

    @pytest.mark.asyncio
    async def test_update_with_some_updated_data(
        self,
        fake_unit_of_work,
        fake_document_repository_class,
    ):
        update_serach_data = Mock()
        update_serach_data.id = 1
        update_serach_data.cypher = None
        update_serach_data.fund = "new fund"
        update_serach_data.inventory = None
        update_serach_data.case = "new case"
        update_serach_data.leaf = None
        update_serach_data.authenticity = "new authenticity"
        update_serach_data.lang = None
        update_serach_data.playback_method = "new playback method"
        update_serach_data.other = None
        update_data = Mock()

        update_data.file_url = None
        update_data.author = "new author"
        update_data.dating = None
        update_data.place_of_creating = "new almaty"
        update_data.variety = None
        update_data.addressee = "new addressee"
        update_data.brief_content = None
        update_data.case_prod_number = "new case prod number"
        update_data.main_text = None
        update_data.search_data = update_serach_data

        uow = fake_unit_of_work(repository=fake_document_repository_class)
        service = DocumentService()

        m_open = mock_open()

        with patch('builtins.open', m_open), patch('os.rename') as mock_rename:
            document = await service.update_document(id=1, file=None, data=update_data, uow=uow)

            assert document.id == 1
            assert isinstance(document.created_at, datetime)
            assert document.file_url == "test_url.pdf"
            assert document.author == "new author"
            assert document.dating == "2020"
            assert document.place_of_creating == "new almaty"
            assert document.variety == "varietry"
            assert document.addressee == "new addressee"
            assert document.brief_content == "brief content"
            assert document.case_prod_number == "new case prod number"
            assert document.main_text == "main text"

            assert document.search_data.id == 1
            assert document.search_data.cypher == "cypher"
            assert document.search_data.fund == "new fund"
            assert document.search_data.inventory == "inventory"
            assert document.search_data.case == "new case"
            assert document.search_data.leaf == "leaf"
            assert document.search_data.authenticity == "new authenticity"
            assert document.search_data.lang == "lang"
            assert document.search_data.playback_method == "new playback method"
            assert document.search_data.other == "other"

            with pytest.raises(AssertionError) as rename_error:
                mock_rename.assert_called_once_with("files/test_url.pdf", "files/new_test_url.pdf")
          
            with pytest.raises(AssertionError) as error:
                m_open.assert_called_once_with(f"files/{document.file_url}", "wb")             
                handle = m_open()
                handle.write.assert_called_once_with(b'new file_bytes')

            assert str(error.value) == "Expected 'open' to be called once. Called 0 times."
    
    @pytest.mark.asyncio
    async def test_delete_document(
            self,
            fake_unit_of_work,
            fake_document_repository_class,
            upload_document_mock
    ):
        uow = fake_unit_of_work(repository=fake_document_repository_class)
        service = DocumentService()

        with patch('os.remove') as mock_remove:
            await service.delete_document(id=upload_document_mock.id, uow=uow)
            mock_remove.assert_called_once_with(f"files/{upload_document_mock.file_url}")
