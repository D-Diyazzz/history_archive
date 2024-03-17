from sqlalchemy import (
    MetaData, 
    Table, 
    Column, 
    BigInteger, 
    String, 
    Integer,
    ForeignKey,
    Text,
    DateTime,
)
from sqlalchemy.orm import registry, relationship

from src.archive.domains.Type import TypeCollection
from src.archive.domains.Class_collection import ClassCollection
from src.archive.domains.Form_collection import FormCollection
from src.archive.domains.Method_collection import MethodCollection
from src.archive.domains.collection import Collection


mapper_registry = registry()


type_collection = Table(
    "type_coll",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),
    Column("name", String(250), nullable=False, unique=True)
)

class_collection = Table(
    "class_coll",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("name", String(250), nullable=False, unique=True)
)

form_collection = Table(
    "format_coll",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("name", String(250), nullable=False, unique=True)
)

method_collection = Table(
    "method_coll",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("name", String(250), nullable=False, unique=True)
)

collection = Table(
    "collection",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("file_url", Text, nullable=False),
    Column("theme", String(700), nullable=False),
    Column("purpose", String(500), nullable=False),
    Column("task", String(1000), nullable=False),
    Column("type_id", BigInteger, ForeignKey("type_coll.id"), nullable=False),
    Column("class_id", BigInteger, ForeignKey("class_coll.id"), nullable=False),
    Column("format_id", BigInteger, ForeignKey("format_coll.id"), nullable=False),
    Column("method_id", BigInteger, ForeignKey("method_coll.id"), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),

    Column("preface", Text, nullable=True),
    Column("note", Text, nullable=True),
    Column("indication", Text, nullable=True),
    Column("intro_text", Text, nullable=True),
    Column("recommendations", Text, nullable=True),
)

def start_mappers():
    mapper_registry.map_imperatively(TypeCollection, type_collection)
    mapper_registry.map_imperatively(ClassCollection, class_collection)
    mapper_registry.map_imperatively(FormCollection, form_collection)
    mapper_registry.map_imperatively(MethodCollection, method_collection)
    mapper_registry.map_imperatively(
        Collection, 
        collection, 
        properties={
            "type_coll": relationship(TypeCollection, uselist=False, backref="collection"),
            "class_coll": relationship(ClassCollection, uselist=False, backref="collection"),
            "form_coll": relationship(FormCollection, uselist=False, backref="collection"),
            "method_coll": relationship(MethodCollection, uselist=False, backref="collection"),
        }
    )