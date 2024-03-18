from fastapi import FastAPI

from src.archive.gateway.urls import (
    get_type_collection_router,
    get_class_collection_router,
    get_form_collection_router,
    get_method_collection_router,
    get_collection_router,
    get_document_router
)
from src.archive.database import start_mappers


app = FastAPI(
    title="Archive",
)

start_mappers()


app.include_router(get_type_collection_router())
app.include_router(get_class_collection_router())
app.include_router(get_form_collection_router())
app.include_router(get_method_collection_router())
app.include_router(get_collection_router())
app.include_router(get_document_router())