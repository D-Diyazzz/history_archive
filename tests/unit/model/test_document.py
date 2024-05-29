import pytest
import pytz

from datetime import datetime

from src.archive.domains.document import Document, SearchData


class TestUnitDocumentModel:
    def test_init_document_model(self, init_search_data):
        document = Document(
            file_urls=["file_url1.pdf", "file_url2.pdf"],
            author="author",
            dating="2018",
            place_of_creating="almaty",
            variety="variety",
            addressee="addressee",
            brief_content="brief content",
            case_prod_number="case production number",
            main_text="main text",
            search_data=init_search_data
        )

        assert document.id is None
        assert isinstance(document.created_at, datetime)
        assert document.file_urls == ["file_url1.pdf", "file_url2.pdf"]
        assert document.author == "author"
        assert document.dating == "2018"
        assert document.place_of_creating == "almaty"
        assert document.variety == "variety"
        assert document.addressee == "addressee"
        assert document.brief_content == "brief content"
        assert document.case_prod_number == "case production number"
        assert document.main_text == "main text"

        assert document.search_data.id is None
        assert document.search_data.cypher == "cypher"
        assert document.search_data.fund == "fund"
        assert document.search_data.inventory == "inventory"
        assert document.search_data.case == "case"
        assert document.search_data.leaf == "leaf"
        assert document.search_data.authenticity == "authenticity"
        assert document.search_data.lang == "lang"
        assert document.search_data.playback_method == "playback method"
        assert document.search_data.other is None

    def test_upload_document_model(self, upload_search_data):
        time = datetime.now(pytz.UTC)

        document = Document(
            id = 1,
            file_urls=["file_url1.pdf", "file_url2.pdf"],
            author="author",
            dating="2018",
            place_of_creating="almaty",
            variety="variety",
            addressee="addressee",
            brief_content="brief content",
            case_prod_number="case production number",
            main_text="main text",
            created_at=time,
            search_data=upload_search_data
        )

        assert document.id is 1
        assert document.created_at == time
        assert document.file_urls == ["file_url1.pdf", "file_url2.pdf"]
        assert document.author == "author"
        assert document.dating == "2018"
        assert document.place_of_creating == "almaty"
        assert document.variety == "variety"
        assert document.addressee == "addressee"
        assert document.brief_content == "brief content"
        assert document.case_prod_number == "case production number"
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