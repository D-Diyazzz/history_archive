from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.archive.gateway.urls import (
    get_collection_router,
    get_document_router,
    get_auth_router,
)
from src.archive.database import start_mappers


app = FastAPI(
    title="Archive",
)

origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://127.0.0.1:5173",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/archive/files", StaticFiles(directory="files"), name="static")

start_mappers()

app.include_router(get_collection_router())
app.include_router(get_document_router())
app.include_router(get_auth_router())
