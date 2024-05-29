import pytest
import pytz

from datetime import datetime

from src.archive.domains.document import PhonoDocument


class TestUnitPhonoDocumentModel:
    def test_init_photo_document_model(self):
        document = PhonoDocument(
            file_urls=["file_url1.pdf", "file_url2.pdf"],
            author="author",
            dating="2018",
            place_of_creating="almaty",
            genre="genre",
            brief_summary="brief summary",
            addressee="addressee",
            cypher="cypher",
            lang="lang",
            storage_media="storage media",
        )

        assert document.id is None
        assert isinstance(document.created_at, datetime)
        assert document.file_urls == ["file_url1.pdf", "file_url2.pdf"]
        assert document.author == "author"
        assert document.dating == "2018"
        assert document.place_of_creating == "almaty"
        assert document.genre == "genre"
        assert document.brief_summary == "brief summary"
        assert document.addressee == "addressee"
        assert document.cypher == "cypher"
        assert document.lang == "lang"
        assert document.storage_media == "storage media"

    def test_upload_photo_document_model(self):
        time = datetime.now(pytz.UTC)

        document = PhonoDocument(
            id = 1,
            file_urls=["file_url1.pdf", "file_url2.pdf"],
            author="author",
            dating="2018",
            place_of_creating="almaty",
            genre="genre",
            brief_summary="brief summary",
            addressee="addressee",
            cypher="cypher",
            lang="lang",
            storage_media="storage media",
            created_at=time,
        )

        assert document.id is 1
        assert document.created_at == time
        assert document.file_urls == ["file_url1.pdf", "file_url2.pdf"]
        assert document.author == "author"
        assert document.dating == "2018"
        assert document.place_of_creating == "almaty"
        assert document.genre == "genre"
        assert document.brief_summary == "brief summary"
        assert document.addressee == "addressee"
        assert document.cypher == "cypher"
        assert document.lang == "lang"
        assert document.storage_media == "storage media"