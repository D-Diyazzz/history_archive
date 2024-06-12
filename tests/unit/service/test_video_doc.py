import pytest

from unittest.mock import Mock, mock_open, patch, call
from datetime import datetime

from src.archive.service.document import VideoDocumentService


@pytest.fixture
def init_videodocument_mock(init_search_data_mock):
    data = Mock()
    data.author = "author"
    data.dating = "2020"
    data.place_of_creating = "almaty"
    data.title = "title"
    data.volume = "volume"
    data.num_of_parts = "num of parts"
    data.color = "color"
    data.creator = "creator"
    data.info_of_publication = "info of publication"
    data.search_data = init_search_data_mock
    return data

@pytest.fixture
def upload_videodocument_mock(upload_search_data_mock, id=1):
    data = Mock()
    data.id = id
    data.author = "author"
    data.dating = "2020"
    data.place_of_creating = "almaty"
    data.title = "title"
    data.volume = "volume"
    data.num_of_parts = "num of parts"
    data.color = "color"
    data.creator = "creator"
    data.info_of_publication = "info of publication"
    data.search_data = upload_search_data_mock
    return data


class TestUnitVideoDocService:

    @pytest.mark.asyncio
    async def test_create_document(
            self,
            fake_unit_of_work,
            fake_videodocument_repository_class,
            init_videodocument_mock
    ):
        uow = fake_unit_of_work(repository=fake_videodocument_repository_class)
        service = VideoDocumentService()

        m_open = mock_open()

        with patch('builtins.open', m_open):
            files = {
                "file_url_1.mp4": b'file_bytes_1',
                "file_url_2.mp4": b'file_bytes_2'
            }
            document = await service.create_document(files=files, data=init_videodocument_mock, uow=uow)

            assert document.id == 1
            assert isinstance(document.created_at, datetime)
            assert document.file_urls == ["file_url_1.mp4", "file_url_2.mp4"]
            assert document.author == "author"
            assert document.dating == "2020"
            assert document.place_of_creating == "almaty"
            assert document.title == "title"
            assert document.volume == "volume"
            assert document.num_of_parts == "num of parts"
            assert document.color == "color"
            assert document.creator == "creator"
            assert document.info_of_publication == "info of publication"

            assert document.search_data.id == 1
            assert document.search_data.cypher == "cypher"
            assert document.search_data.fund == "fund"
            assert document.search_data.inventory == "inventory"
            assert document.search_data.case == "case"
            assert document.search_data.leaf == "leaf"
            assert document.search_data.authenticity == "authenticity"
            assert document.search_data.lang == "lang"
            assert document.search_data.playback_method == "playback method"
            assert document.search_data.other is None

            m_open.assert_has_calls([
                call(f"files/file_url_1.mp4", "wb"),
                call(f"files/file_url_2.mp4", "wb")
            ], any_order=True)

            handle_1 = m_open()
            handle_1.write.assert_any_call(b'file_bytes_1')

            handle_2 = m_open()
            handle_2.write.assert_any_call(b'file_bytes_2') 


    @pytest.mark.asyncio
    async def test_update_with_file_document(
        self,
        fake_unit_of_work,
        fake_videodocument_repository_class,
        upload_search_data_mock
    ):
        update_data = Mock()

        update_data.author = "new author"
        update_data.dating = "new 2020"
        update_data.place_of_creating = "new almaty"
        update_data.title = "new title"
        update_data.volume = "new volume"
        update_data.num_of_parts = "new num of parts"
        update_data.color = "new color"
        update_data.creator = "new creator"
        update_data.info_of_publication = "new info of publication"
        update_data.search_data = upload_search_data_mock

        uow = fake_unit_of_work(repository=fake_videodocument_repository_class)
        service = VideoDocumentService()

        m_open = mock_open()

        files = {
            "new_file_url_1.mp4": b'new_file_bytes_1',
            "new_file_url_2.mp4": b'new_file_bytes_2'
        }

        with patch('builtins.open', m_open), patch('os.remove') as mock_remove:
            document = await service.update_document(id=1, files=files, data=update_data, uow=uow)

            assert document.id == 1
            assert isinstance(document.created_at, datetime)
            assert document.file_urls == ["new_file_url_1.mp4", "new_file_url_2.mp4"]
            assert document.author == "new author"
            assert document.dating == "new 2020"
            assert document.place_of_creating == "new almaty"
            assert document.title == "new title"
            assert document.volume == "new volume"
            assert document.num_of_parts == "new num of parts"
            assert document.color == "new color"
            assert document.creator == "new creator"
            assert document.info_of_publication == "new info of publication"

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

            mock_remove.assert_has_calls([
                call("files/file_url_1.mp4"),
                call("files/file_url_2.mp4")
            ], any_order=True)

            m_open.assert_has_calls([
                call(f"files/new_file_url_1.mp4", "wb"),
                call(f"files/new_file_url_2.mp4", "wb")
            ], any_order=True)

            handle_1 = m_open()
            handle_1.write.assert_any_call(b'new_file_bytes_1')

            handle_2 = m_open()
            handle_2.write.assert_any_call(b'new_file_bytes_2')


    @pytest.mark.asyncio
    async def test_update_without_file_document(
        self,
        fake_unit_of_work,
        fake_videodocument_repository_class,
        upload_search_data_mock
    ):
        update_data = Mock()

        update_data.author = "new author"
        update_data.dating = "new 2020"
        update_data.place_of_creating = "new almaty"
        update_data.title = "new title"
        update_data.volume = "new volume"
        update_data.num_of_parts = "new num of parts"
        update_data.color = "new color"
        update_data.creator = "new creator"
        update_data.info_of_publication = "new info of publication"
        update_data.search_data = upload_search_data_mock

        uow = fake_unit_of_work(repository=fake_videodocument_repository_class)
        service = VideoDocumentService()

        m_open = mock_open()

        with patch('builtins.open', m_open), patch('os.remove') as mock_remove:
            document = await service.update_document(id=1, files=None, data=update_data, uow=uow)

            assert document.id == 1
            assert isinstance(document.created_at, datetime)
            assert document.file_urls == ["file_url_1.mp4", "file_url_2.mp4"]
            assert document.author == "new author"
            assert document.dating == "new 2020"
            assert document.place_of_creating == "new almaty"
            assert document.title == "new title"
            assert document.volume == "new volume"
            assert document.num_of_parts == "new num of parts"
            assert document.color == "new color"
            assert document.creator == "new creator"
            assert document.info_of_publication == "new info of publication"

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

            with pytest.raises(AssertionError) as error:
                mock_remove.assert_has_calls([
                    call("files/file_url_1.mp4"),
                    call("files/file_url_2.mp4")
                ], any_order=True)

            with pytest.raises(AssertionError) as error:
                m_open.assert_called_once_with(f"files/new_test_url", "wb")
                handle = m_open()
                handle.write.assert_called_once_with(b'new file_bytes')

            assert str(error.value) == "Expected 'open' to be called once. Called 0 times."


    @pytest.mark.asyncio
    async def test_update_with_updated_search_data_document(
        self,
        fake_unit_of_work,
        fake_videodocument_repository_class,
    ):
        update_search_data = Mock()
        update_search_data.id = 1
        update_search_data.cypher = "new cypher"
        update_search_data.fund = "new fund"
        update_search_data.inventory = "new inventory"
        update_search_data.case = "new case"
        update_search_data.leaf = "new leaf"
        update_search_data.authenticity = "new authenticity"
        update_search_data.lang = "new lang"
        update_search_data.playback_method = "new playback method"
        update_search_data.other = "new other"
        update_data = Mock()

        update_data.author = "new author"
        update_data.dating = "new 2020"
        update_data.place_of_creating = "new almaty"
        update_data.title = "new title"
        update_data.volume = "new volume"
        update_data.num_of_parts = "new num of parts"
        update_data.color = "new color"
        update_data.creator = "new creator"
        update_data.info_of_publication = "new info of publication"
        update_data.search_data = update_search_data

        uow = fake_unit_of_work(repository=fake_videodocument_repository_class)
        service = VideoDocumentService()

        m_open = mock_open()

        files = {
            "file_url_1.mp4": b'file_bytes_1',
            "new_file_url_2.mp4": b'new_file_bytes_2'
        }

        with patch('builtins.open', m_open), patch('os.remove') as mock_remove:
            document = await service.update_document(id=1, files=files, data=update_data, uow=uow)

            assert document.id == 1
            assert isinstance(document.created_at, datetime)
            assert document.file_urls == ["file_url_1.mp4", "new_file_url_2.mp4"]
            assert document.author == "new author"
            assert document.dating == "new 2020"
            assert document.place_of_creating == "new almaty"
            assert document.title == "new title"
            assert document.volume == "new volume"
            assert document.num_of_parts == "new num of parts"
            assert document.color == "new color"
            assert document.creator == "new creator"
            assert document.info_of_publication == "new info of publication"

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

            mock_remove.assert_has_calls([
                call("files/file_url_1.mp4"),
                call("files/file_url_2.mp4")
            ], any_order=True)

            m_open.assert_has_calls([
                call(f"files/file_url_1.mp4", "wb"),
                call(f"files/new_file_url_2.mp4", "wb")
            ], any_order=True)

            handle_1 = m_open()
            handle_1.write.assert_any_call(b'file_bytes_1')

            handle_2 = m_open()
            handle_2.write.assert_any_call(b'new_file_bytes_2')


    @pytest.mark.asyncio
    async def test_delete_document(
            self,
            fake_unit_of_work,
            fake_videodocument_repository_class,
            upload_videodocument_mock
    ):
        uow = fake_unit_of_work(repository=fake_videodocument_repository_class)
        service = VideoDocumentService()

        with patch('os.remove') as mock_remove:
            await service.delete_document(id=upload_videodocument_mock.id, uow=uow)
            mock_remove.assert_has_calls([
                call("files/file_url_1.mp4"),
                call("files/file_url_2.mp4")
            ], any_order=True)
