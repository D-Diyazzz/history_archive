from sqlalchemy.ext.asyncio import AsyncSession

from src.archive.repository.collection.repostiory import CollectionRepository
from src.archive.repository.collection_comment.repository import CollectionCommentRepository
from src.archive.repository.document.doc_repository import DocumentRepository
from src.archive.repository.document.phono_doc_repository import PhonoDocumentRepository
from src.archive.repository.document.photo_doc_repository import PhotoDocumentRepository
from src.archive.repository.document.video_doc_repository import VideoDocumentRepository
from src.archive.repository.document_links.repository import DocumentsLinkRepostiory
from src.archive.repository.notification.collection_notification_repository import CollectionNotificationRepository
from src.archive.repository.user.repository import UserRepository
from src.archive.repository.user_links.collection_user_group_repository import CollectionUserGroupRepository
from src.archive.repository.user_links import SciCouncilGroupCollectionLinkRepository, RedactorGroupCollectionLinkRepository

from src.archive.domains.collection import Collection
from src.archive.domains.notification import CollectionNotification
from src.archive.domains.user_link import SciCouncilGroupCollectionLink, RedactorGroupCollectionLink


class RepositoryFactory:

    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    def get_repository(self, obj_type):
        print(obj_type == CollectionNotification)
        if obj_type == Collection:
            return CollectionRepository(self.session_factory)
        elif obj_type == CollectionCommentRepository:
            return CollectionCommentRepository(self.session_factory)
        elif obj_type == DocumentRepository:
            return DocumentRepository(self.session_factory)
        elif obj_type == PhonoDocumentRepository:
            return PhonoDocumentRepository(self.session_factory)
        elif obj_type == PhotoDocumentRepository:
            return PhotoDocumentRepository(self.session_factory)
        elif obj_type == VideoDocumentRepository:
            return VideoDocumentRepository(self.session_factory)
        elif obj_type == DocumentsLinkRepostiory:
            return DocumentsLinkRepostiory(self.session_factory)
        elif obj_type == CollectionNotification:
            return CollectionNotificationRepository(self.session_factory)
        elif obj_type == UserRepository:
            return UserRepository(self.session_factory)
        elif obj_type == SciCouncilGroupCollectionLink:
            return SciCouncilGroupCollectionLinkRepository(self.session_factory)
        elif obj_type == RedactorGroupCollectionLink:
            return RedactorGroupCollectionLinkRepository(self.session_factory)

