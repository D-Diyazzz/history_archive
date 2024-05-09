import pytest
import os

from unittest.mock import MagicMock, mock_open, AsyncMock, patch
from datetime import datetime

from src.archive.domains.document import Document, SearchData
from src.archive.service.document import DocumentService


@pytest.fixture
def init_document_mock(init_search_data):

    data = MagicMock()
    data.file_url = "test_url.pdf"
    data.author = "author"
    data.dating = "2020"
    data.place_of_creating = "almaty"
    data.variety = "variety"
    data.addressee = "addressee"
    data.brief_content = "brief content"
    data.case_prod_number = "case prod number"
    data.main_text = "main text"
    data.search_data = init_search_data

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
            assert document.search_data.other == "other"

            m_open.assert_called_once_with(f"files/{document.file_url}", "wb")             
            handle = m_open()
            handle.write.assert_called_once_with(b'file_bytes')
