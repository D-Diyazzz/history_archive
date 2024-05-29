import pytest
import pytz

from datetime import datetime

from src.archive.domains.document import VideoDocument


class TestUnitVideoDocumentModel:
    def test_init_photo_document_model(self, init_search_data):
        document = VideoDocument(
            file_urls=["file_url1.pdf", "file_url2.pdf"],
            author="author",
            dating="2018",
            place_of_creating="almaty",
            title="title",
            volume="volume",
            num_of_parts="num_of_parts",
            color="color",
            creator="creator",
            info_of_publication="info_of_publication",
            search_data=init_search_data
        )

        assert document.id is None
        assert isinstance(document.created_at, datetime)
        assert document.file_urls == ["file_url1.pdf", "file_url2.pdf"]
        assert document.author == "author"
        assert document.dating == "2018"
        assert document.place_of_creating == "almaty"
        assert document.title == "title"
        assert document.volume == "volume"
        assert document.num_of_parts == "num_of_parts"
        assert document.color == "color"
        assert document.info_of_publication == "info_of_publication"
        assert document.creator == "creator"

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

    def test_upload_photo_document_model(self, upload_search_data):
        time = datetime.now(pytz.UTC)

        document = VideoDocument(
            id = 1,
            file_urls=["file_url1.pdf", "file_url2.pdf"],
            author="author",
            dating="2018",
            place_of_creating="almaty",
            title="title",
            volume="volume",
            num_of_parts="num_of_parts",
            color="color",
            creator="creator",
            info_of_publication="info_of_publication",
            created_at=time,
            search_data=upload_search_data
        )

        assert document.id is 1
        assert document.created_at == time
        assert document.file_urls == ["file_url1.pdf", "file_url2.pdf"]
        assert document.author == "author"
        assert document.dating == "2018"
        assert document.place_of_creating == "almaty"
        assert document.title == "title"
        assert document.volume == "volume"
        assert document.num_of_parts == "num_of_parts"
        assert document.color == "color"
        assert document.info_of_publication == "info_of_publication"
        assert document.creator == "creator"

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