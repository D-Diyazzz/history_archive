from fastapi import FastAPI

from src.archive.gateway.urls import get_type_collection_router
from src.archive.database import start_mappers


app = FastAPI(
    title="Archive",
)

start_mappers()


app.include_router(get_type_collection_router())