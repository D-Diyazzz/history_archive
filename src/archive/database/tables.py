from enum import unique
import uuid

from pytz import timezone
from sqlalchemy import (
    Boolean,
    MetaData, 
    Table, 
    Column, 
    BigInteger, 
    String, 
    Integer,
    ForeignKey,
    Text,
    DateTime,
    Enum,
    JSON
)
from sqlalchemy.orm import registry, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.archive.domains.user import User, Role


mapper_registry = registry()


collection = Table(
    "collection",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True,index=True),
    Column("file_url", Text, nullable=False),
    Column("html_url", Text, nullable=False),
    Column("theme", String(700), nullable=False),
    Column("title", String(700), nullable=False),
    Column("author_id", UUID(as_uuid=True), ForeignKey("user.id"), nullable=False),
    Column("hash_code", String(7), nullable=False, unique=True),
    Column("is_approved", Boolean, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),

)

scientific_council_group = Table(
    "scientific_council_group",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("collection_id",  UUID(as_uuid=True), ForeignKey("collection.id", ondelete="CASCADE"), nullable=False),
    Column("scientific_council_id",  UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False)
)

redactor_group = Table(
    "redactor_group",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("collection_id",  UUID(as_uuid=True), ForeignKey("collection.id", ondelete="CASCADE"), nullable=False),
    Column("redactor_id",  UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False)
)

notification_collection = Table(
    "notification_collection",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("collection_id",  UUID(as_uuid=True), ForeignKey("collection.id", ondelete="CASCADE"), nullable=False),
    Column("user_id",  UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("text", Text, nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False)
)

# documents = Table(
#     "documents",
#     mapper_registry.metadata,
#     Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
#     Column("file_url", Text, nullable=False),
#     Column("title", String(700), nullable=False),
#     Column("heading", String(500), nullable=False),
#     Column("author", String(500), nullable=False),
#     Column("description_content", String(1000), nullable=False),
#     Column("dating", String(255), nullable=False),
#     Column("legends", Text, nullable=False),
#     Column("format_doc", String(500), nullable=False),
#     Column("color_palette", String(500), nullable=False),
#     Column("resolution", String(500), nullable=False),
#     Column("compression", String(500), nullable=False),
#     Column("scanner_model", String(500), nullable=False),
#     Column("created_at", DateTime(timezone=True), nullable=False)
# )

documents = Table(
    "documents",
    mapper_registry.metadata,
    Column("id",  UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True,index=True),
    Column("search_data_id", BigInteger, ForeignKey("search_data.id", ondelete="CASCADE"), nullable=False),
    Column("file_urls", JSON, nullable=False),
    Column("author", String(500), nullable=False),
    Column("dating", String(255), nullable=False),
    Column("place_of_creating", String(500), nullable=False),
    Column("variety", String(255), nullable=False),
    Column("addressee", String(500), nullable=False),
    Column("brief_content", Text, nullable=False),
    Column("case_prod_number", String(255), nullable=False),
    Column("main_text", Text, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False)
)

document_links = Table(
    "document_links",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("collection_id", UUID(as_uuid=True), ForeignKey("collection.id", ondelete="CASCADE"), nullable=False),
    Column("document_id", UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False),
    Column("sequence_number", Integer, nullable=False)
)

photo_documents = Table(
    "photo_documents",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True,index=True),
    Column("search_data_id", BigInteger, ForeignKey("search_data.id", ondelete="CASCADE"), nullable=False),
    Column("file_urls", JSON, nullable=False),
    Column("author", String(500), nullable=False),
    Column("dating", String(255), nullable=False),
    Column("place_of_creating", String(500), nullable=False),
    Column("title", String(500), nullable=False),
    Column("completeness_of_reproduction", String(500), nullable=False),
    Column("storage_media", String(255), nullable=False),
    Column("color", String(255), nullable=False),
    Column("size_of_original", String(255), nullable=False),
    Column("image_scale", String(255), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False)
)

photo_document_links = Table(
    "photo_document_links",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("collection_id", UUID(as_uuid=True), ForeignKey("collection.id", ondelete="CASCADE"), nullable=False),
    Column("photo_document_id", UUID(as_uuid=True), ForeignKey("photo_documents.id", ondelete="CASCADE"), nullable=False),
    Column("sequence_number", Integer, nullable=False)
)

video_documents = Table(
    "video_documents",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True,index=True), 
    Column("search_data_id", BigInteger, ForeignKey("search_data.id", ondelete="CASCADE"), nullable=False),
    Column("file_urls", JSON, nullable=False),
    Column("author", String(500), nullable=False),
    Column("dating", String(255), nullable=False),
    Column("place_of_creating", String(500), nullable=False),
    Column("title", String(500), nullable=False),
    Column("volume", String(255), nullable=False),
    Column("num_of_parts", String(255), nullable=False),
    Column("color", String(255), nullable=False),
    Column("creator", String(500), nullable=False),
    Column("info_of_publication", Text, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False)
)

video_document_links = Table(
    "video_document_links",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("collection_id", UUID(as_uuid=True), ForeignKey("collection.id", ondelete="CASCADE"), nullable=False),
    Column("video_document_id", UUID(as_uuid=True), ForeignKey("video_documents.id", ondelete="CASCADE"), nullable=False),
    Column("sequence_number", Integer, nullable=False)
)

phono_documents = Table(
    "phono_documents",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True,index=True),
    Column("file_urls", JSON, nullable=False),
    Column("author", String(500), nullable=False),
    Column("dating", String(255), nullable=False),
    Column("place_of_creating", String(500), nullable=False),
    Column("genre", String(255), nullable=False),
    Column("brief_summary", String(500), nullable=False),
    Column("addressee", String(500), nullable=False),
    Column("cypher", String(255), nullable=False),
    Column("lang", String(255), nullable=False),
    Column("storage_media", String(255), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False)
)

phono_document_links = Table(
    "phono_document_links",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("collection_id", UUID(as_uuid=True), ForeignKey("collection.id", ondelete="CASCADE"), nullable=False),
    Column("phono_document_id", UUID(as_uuid=True), ForeignKey("phono_documents.id", ondelete="CASCADE"), nullable=False),
    Column("sequence_number", Integer, nullable=False)
)

search_data = Table(
    "search_data",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("cypher", String(255), nullable=False),
    Column("fund", String(255), nullable=False),
    Column("inventory", String(255), nullable=False),
    Column("case", String(255), nullable=False),
    Column("leaf", String(255), nullable=False),
    Column("authenticity", String(255), nullable=False),
    Column("lang", String(255), nullable=False),
    Column("playback_method", String(500), nullable=False),
    Column("other", Text, nullable=True)
)

user = Table(
    "user",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True,index=True),
    Column("firstname", String(250), nullable=False),
    Column("lastname", String(250), nullable=False),
    Column("email", String(250), nullable=False, unique=True, index=True),
    Column("role", Enum(Role), nullable=False),
    Column("hashed_password", Text, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False)
)


def start_mappers():
    mapper_registry.map_imperatively(User, user)
