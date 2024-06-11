import pytest

from unittest.mock import Mock, mock_open, patch, call
from datetime import datetime

from src.archive.core import repository
from src.archive.domains.document import PhonoDocument
from src.archive.service.document import PhonoDocumentService


@pytest.fixture
def init_phonodocument_mock():
    data = Mock()
    data.author = "author"
    data.dating = "2020"
    data.place_of_creating = "almaty"
    data.genre = "genre"
    data.brief_summary = "brief summary"
    data.addressee = "addressee"
    data.cypher = "cypher"
    data.lang = "lang"
    data.storage_media = "storage media"

    return data

@pytest.fixture
def upload_phonodocument_mock(id=1):
    data = Mock()
    data.id = id
    data.author = "author"
    data.dating = "2020"
    data.place_of_creating = "almaty"
    data.genre = "genre"
    data.brief_summary = "brief summary"
    data.addressee = "addressee"
    data.cypher = "cypher"
    data.lang = "lang"
    data.storage_media = "storage media"

    return data


class TestUnitPhonoDocService:

    @pytest.mark.asyncio
    async def test_create_phono_doc(
            self,
            fake_unit_of_work,
            fake_phonodocument_repository_class,
            init_phonodocument_mock,
    ):
        uow = fake_unit_of_work(repository=fake_phonodocument_repository_class)
        service = PhonoDocumentService()

        m_open = mock_open()

        with patch('builtins.open', m_open):
            files = {
                "file_url_1.mp3": b'file_bytes_1',
                "file_url_2.mp3": b'file_bytes_2',
            }

            document = await service.create_document(
                files=files,
                data=init_phonodocument_mock,
                uow=uow
            )
            
            assert document.id == 1 
            assert isinstance(document.created_at, datetime)
            assert document.file_urls == ["file_url_1.mp3", "file_url_2.mp3"]
            assert document.author == "author"
            assert document.dating == "2020"
            assert document.place_of_creating == "almaty"
            assert document.genre == "genre"
            assert document.brief_summary == "brief summary"
            assert document.addressee == "addressee"
            assert document.cypher == "cypher"
            assert document.lang == "lang"
            assert document.storage_media == "storage media"

            m_open.assert_has_calls([
                call(f"files/file_url_1.mp3", "wb"),
                call(f"files/file_url_2.mp3", "wb")
            ], any_order=True)

            handle_1 = m_open()
            handle_1.write.assert_any_call(b'file_bytes_1')

            handle_2 = m_open()
            handle_2.write.assert_any_call(b'file_bytes_2')
    

    @pytest.mark.asyncio
    async def test_update_with_file_document(
        self,
        fake_unit_of_work,
        fake_phonodocument_repository_class,
    ):
        update_data = Mock()
        update_data.author = "new author"
        update_data.dating = "new 2020"
        update_data.place_of_creating = "new almaty"
        update_data.genre = "new genre"
        update_data.brief_summary = "new brief summary"
        update_data.addressee = "new addressee"
        update_data.cypher = "new cypher"
        update_data.lang = "new lang"
        update_data.storage_media = "new storage media"

        uow = fake_unit_of_work(repository=fake_phonodocument_repository_class)
        service = PhonoDocumentService()

        m_open = mock_open()

        files = {
            "new_file_url_1.mp3": b'new_file_bytes_1',
            "new_file_url_2.mp3": b'new_file_bytes_2',
        }

        with patch('builtins.open', m_open), patch('os.remove') as mock_remove:
            document = await service.update_document(
                id=1,
                files=files,
                data=update_data,
                uow=uow
            )

            assert document.id == 1 
            assert isinstance(document.created_at, datetime)
            assert document.file_urls == ["new_file_url_1.mp3", "new_file_url_2.mp3"]
            assert document.author == "new author"
            assert document.dating == "new 2020"
            assert document.place_of_creating == "new almaty"
            assert document.genre == "new genre"
            assert document.brief_summary == "new brief summary"
            assert document.addressee == "new addressee"
            assert document.cypher == "new cypher"
            assert document.lang == "new lang"
            assert document.storage_media == "new storage media"

            mock_remove.assert_has_calls([
                call("files/file_url_1.mp3"),
                call("files/file_url_2.mp3")
            ], any_order=True)

            m_open.assert_has_calls([
                call(f"files/new_file_url_1.mp3", "wb"),
                call(f"files/new_file_url_2.mp3", "wb")
            ], any_order=True)

            handle_1 = m_open()
            handle_1.write.assert_any_call(b'new_file_bytes_1')

            handle_2 = m_open()
            handle_2.write.assert_any_call(b'new_file_bytes_2')


    @pytest.mark.asyncio
    async def test_update_without_file_document(
        self,
        fake_unit_of_work,
        fake_phonodocument_repository_class,
    ):
        update_data = Mock()
        update_data.author = "new author"
        update_data.dating = "new 2020"
        update_data.place_of_creating = "new almaty"
        update_data.genre = "new genre"
        update_data.brief_summary = "new brief summary"
        update_data.addressee = "new addressee"
        update_data.cypher = "new cypher"
        update_data.lang = "new lang"
        update_data.storage_media = "new storage media"

        uow = fake_unit_of_work(repository=fake_phonodocument_repository_class)
        service = PhonoDocumentService()

        m_open = mock_open()

        with patch('builtins.open', m_open), patch('os.remove') as mock_remove:
            document = await service.update_document(
                id=1,
                files=None,
                data=update_data,
                uow=uow
            )

            assert document.id == 1 
            assert isinstance(document.created_at, datetime)
            assert document.file_urls == ["file_url_1.mp3", "file_url_2.mp3"]
            assert document.author == "new author"
            assert document.dating == "new 2020"
            assert document.place_of_creating == "new almaty"
            assert document.genre == "new genre"
            assert document.brief_summary == "new brief summary"
            assert document.addressee == "new addressee"
            assert document.cypher == "new cypher"
            assert document.lang == "new lang"
            assert document.storage_media == "new storage media"
            
            with pytest.raises(AssertionError) as error:
                mock_remove.assert_has_calls([
                    call("files/file_url_1.mp3"),
                    call("files/file_url_2.mp3")
                ], any_order=True)
            
            with pytest.raises(AssertionError) as error:
                m_open.assert_has_calls([
                    call(f"files/new_file_url_1.mp3", "wb"),
                    call(f"files/new_file_url_2.mp3", "wb")
                ], any_order=True)

            print(error.value)

            assert str(error.value) == "'open' does not contain all of (call('', ('files/new_file_url_1.mp3', 'wb'), {}), call('', ('files/new_file_url_2.mp3', 'wb'), {})) in its call list, found [] instead"



    @pytest.mark.asyncio
    async def test_delete_document(
        self,
        fake_unit_of_work,
        fake_phonodocument_repository_class
    ):
        uow = fake_unit_of_work(repository=fake_phonodocument_repository_class)
        service = PhonoDocumentService()

        with patch('os.remove') as mock_remove:
            await service.delete_document(id=1, uow=uow)
            mock_remove.assert_has_calls([
                call("files/file_url_1.mp3"),
                call("files/file_url_2.mp3")
            ])
