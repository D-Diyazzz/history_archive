from sqlalchemy import (
    MetaData, 
    Table, 
    Column, 
    BigInteger, 
    String, 
    Integer
)
from sqlalchemy.orm import registry

from src.archive.domains.Type import Type
from src.archive.domains.Class_collection import ClassCollection
from src.archive.domains.Form_collection import FormCollection
from src.archive.domains.Method_collection import MethodCollection


mapper_registry = registry()


type_collection = Table(
    "type",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),
    Column("name", String(250), primary_key=True, nullable=False, unique=True)
)

class_collection = Table(
    "class",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("name", String(250), primary_key=True, nullable=False, unique=True)
)

form_collection = Table(
    "form",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("name", String(250), primary_key=True, nullable=False, unique=True)
)

method_collection = Table(
    "method",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("name", String(250), primary_key=True, nullable=False, unique=True)
)


def start_mappers():
    mapper_registry.map_imperatively(Type, type_collection)
    mapper_registry.map_imperatively(ClassCollection, class_collection)
    mapper_registry.map_imperatively(FormCollection, form_collection)
    mapper_registry.map_imperatively(MethodCollection, method_collection)