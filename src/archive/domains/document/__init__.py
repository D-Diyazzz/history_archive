from .document_model import Document
from .photo_document_model import PhotoDocument
from .video_documents_model import VideoDocument
from .phono_document import PhonoDocument
from .abstractions import AbstarctDocument, SearchData


__all__ = [
    "Document",
    "AbstarctDocument",
    "SearchData",
    "PhotoDocument",
    "VideoDocument",
    "PhonoDocument",
]