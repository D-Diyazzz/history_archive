import pytest

from unittest.mock import Mock, mock_open, patch, call
from datetime import datetime

from src.archive.domains.document import PhotoDocument, SearchData
from src.archive.service.document import PhotoDocumentService
from tests.unit.service.conftest import fake_photodocument_repository_class, fake_unit_of_work


@pytest.fixture
def init_photodocument_mock(init_search_data_mock):
    data = Mock()
    data.author = "author"
    data.dating = "2020"
    data.place_of_creating = "almaty"
    data.title = "title"
    data.completeness_of_reproduction = "completeness"
    data.storage_media = "storage media"
    data.color = "color"
    data.size_of_original = "size of original"
    data.image_scale = "image scale"
    data.search_data = init_search_data_mock
    return data

@pytest.fixture
def upload_photodocument_mock(upload_search_data_mock, id=1):
    data = Mock()
    data.id = id
    data.author = "author"
    data.dating = "2020"
    data.place_of_creating = "almaty"
    data.title = "title"
    data.completeness_of_reproduction = "completeness"
    data.storage_media = "storage media"
    data.color = "color"
    data.size_of_original = "size of original"
    data.image_scale = "image scale"
    data.search_data = upload_search_data_mock
    return data


class TestUnitPhotoDocService:

    @pytest.mark.asyncio
    async def test_create_document(
        self,
        fake_unit_of_work,
        fake_photodocument_repository_class,
        init_photodocument_mock
    ):
        uow = fake_unit_of_work(repository=fake_photodocument_repository_class)
        service = PhotoDocumentService()

        m_open = mock_open()
        
        with patch('builtins.open', m_open):
            files = {
                "file_url_1.jpg": b'file_bytes_1',
                "file_url_2.jpg": b'file_bytes_2',
            }

            document = await service.create_document(files=files, data=init_photodocument_mock, uow=uow)

            assert document.id == 1
            assert isinstance(document.created_at, datetime)
            assert document.file_urls == ["file_url_1.jpg", "file_url_2.jpg"]
            assert document.author == "author"
            assert document.dating == "2020"
            assert document.place_of_creating == "almaty"
            assert document.title == "title"
            assert document.completeness_of_reproduction == "completeness"
            assert document.storage_media == "storage media"
            assert document.color == "color"
            assert document.size_of_original == "size of original"
            assert document.image_scale == "image scale"

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
                call(f"files/file_url_1.jpg", "wb"),
                call(f"files/file_url_2.jpg", "wb")
            ], any_order=True)

            handle_1 = m_open()
            handle_1.write.assert_any_call(b'file_bytes_1')

            handle_2 = m_open()
            handle_2.write.assert_any_call(b'file_bytes_2')

    
    @pytest.mark.asyncio
    async def test_update_with_updated_search_data_document(
        self,
        fake_unit_of_work,
        fake_photodocument_repository_class
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
        update_data.author = "new author"
        update_data.dating = "new 2020"
        update_data.place_of_creating = "new almaty"
        update_data.title = "new title"
        update_data.completeness_of_reproduction = "new completeness"
        update_data.storage_media = "new storage media"
        update_data.color = "new color"
        update_data.size_of_original = "new size of original"
        update_data.image_scale = "new image scale"
        update_data.search_data = update_serach_data
        
        uow = fake_unit_of_work(repository=fake_photodocument_repository_class)
        service = PhotoDocumentService()

        m_open = mock_open()

        files = {
            "file_url_1.jpg": b'file_bytes_1',
            "new_file_url_2.jpg": b'new_file_bytes_2'
        }

        with patch('builtins.open', m_open), patch('os.remove') as mock_remove:
            document = await service.update_document(id=1, files=files, data=update_data, uow=uow)

            assert document.id == 1
            assert isinstance(document.created_at, datetime)
            assert document.file_urls == ["file_url_1.jpg", "new_file_url_2.jpg"]
            assert document.author == "new author"
            assert document.dating == "new 2020"
            assert document.place_of_creating == "new almaty"
            assert document.title == "new title"
            assert document.completeness_of_reproduction == "new completeness"
            assert document.storage_media == "new storage media"
            assert document.color == "new color"
            assert document.size_of_original == "new size of original"
            assert document.image_scale == "new image scale"

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
                call("files/file_url_1.jpg"),
                call("files/file_url_2.jpg"),
            ])

            m_open.assert_has_calls([
                call("files/file_url_1.jpg", "wb"),
                call("files/new_file_url_2.jpg", "wb")
            ], any_order=True)

            handle_1 = m_open()
            handle_1.write.assert_any_call(b'file_bytes_1')

            handle_2 = m_open()
            handle_2.write.assert_any_call(b'new_file_bytes_2')


    @pytest.mark.asyncio
    async def test_update_without_file_document(
        self,
        fake_unit_of_work,
        fake_photodocument_repository_class,
        upload_search_data_mock
    ):

        update_data = Mock()
        update_data.author = "new author"
        update_data.dating = "new 2020"
        update_data.place_of_creating = "new almaty"
        update_data.title = "new title"
        update_data.completeness_of_reproduction = "new completeness"
        update_data.storage_media = "new storage media"
        update_data.color = "new color"
        update_data.size_of_original = "new size of original"
        update_data.image_scale = "new image scale"
        update_data.search_data = upload_search_data_mock

        uow = fake_unit_of_work(repository=fake_photodocument_repository_class)
        service = PhotoDocumentService()

        m_open = mock_open()

        with patch('builtins.open', m_open), patch('os.remove') as mock_remove:
            document = await service.update_document(id=1, files=None, data=update_data, uow=uow)    

            assert document.id == 1
            assert isinstance(document.created_at, datetime)
            assert document.file_urls == ["file_url_1.jpg", "file_url_2.jpg"]
            assert document.author == "new author"
            assert document.dating == "new 2020"
            assert document.place_of_creating == "new almaty"
            assert document.title == "new title"
            assert document.completeness_of_reproduction == "new completeness"
            assert document.storage_media == "new storage media"
            assert document.color == "new color"
            assert document.size_of_original == "new size of original"
            assert document.image_scale == "new image scale"
            
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
                    call("files/file_url_1.jpg"),
                    call("files/file_url_2.jpg")
                ], any_order=True)
            
            with pytest.raises(AssertionError) as error:
                m_open.assert_has_calls([
                    call(f"files/new_file_url_1.jpg", "wb"),
                    call(f"files/new_file_url_2.jpg", "wb")
                ], any_order=True)

            assert str(error.value) == "'open' does not contain all of (call('', ('files/new_file_url_1.jpg', 'wb'), {}), call('', ('files/new_file_url_2.jpg', 'wb'), {})) in its call list, found [] instead"


    @pytest.mark.asyncio
    async def test_delete_document(
        self,
        fake_unit_of_work,
        fake_photodocument_repository_class,
    ):
        uow = fake_unit_of_work(repository=fake_photodocument_repository_class)
        service = PhotoDocumentService()

        with patch('os.remove') as mock_remove:
            await service.delete_document(id=1, uow=uow)
            mock_remove.assert_has_calls([
                call("files/file_url_1.jpg"),
                call("files/file_url_2.jpg")
            ])
