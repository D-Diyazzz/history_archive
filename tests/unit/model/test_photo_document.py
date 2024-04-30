import pytest
import pytz

from datetime import datetime

from src.archive.domains.document import PhotoDocument


class TestUnitPhotoDocumentModel:
    def test_init_photo_document_model(self, init_search_data):
        document = PhotoDocument(
            file_url="file_url",
            author="author",
            dating="2018",
            place_of_creating="almaty",
            title="title",
            completeness_of_reproduction="completeness of reproduction",
            storage_media="storage media",
            color="color",
            size_of_original="size of original",
            image_scale="image scale",
            search_data=init_search_data
        )

        assert document.id is None
        assert isinstance(document.created_at, datetime)
        assert document.file_url == "file_url"
        assert document.author == "author"
        assert document.dating == "2018"
        assert document.place_of_creating == "almaty"
        assert document.title == "title"
        assert document.completeness_of_reproduction == "completeness of reproduction"
        assert document.storage_media == "storage media"
        assert document.color == "color"
        assert document.size_of_original == "size of original"
        assert document.image_scale == "image scale"

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

        document = PhotoDocument(
            id = 1,
            file_url="file_url",
            author="author",
            dating="2018",
            place_of_creating="almaty",
            title="title",
            completeness_of_reproduction="completeness of reproduction",
            storage_media="storage media",
            color="color",
            size_of_original="size of original",
            image_scale="image scale",
            created_at=time,
            search_data=upload_search_data
        )

        assert document.id is 1
        assert document.created_at == time
        assert document.file_url == "file_url"
        assert document.author == "author"
        assert document.dating == "2018"
        assert document.place_of_creating == "almaty"
        assert document.title == "title"
        assert document.completeness_of_reproduction == "completeness of reproduction"
        assert document.storage_media == "storage media"
        assert document.color == "color"
        assert document.size_of_original == "size of original"
        assert document.image_scale == "image scale"

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