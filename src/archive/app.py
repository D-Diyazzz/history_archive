from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.archive.gateway.urls import (
    get_collection_router,
    get_document_router,
    get_all_documents_router,
    get_phono_document_router,
    get_auth_router,
    get_user_router,
    get_notification_router,
    get_collection_comment_router,
    get_gpt_router,
)
from src.archive.config import FRONT_URL

app = FastAPI(
    title="Archive",
)

origins = [
    FRONT_URL,
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


app.include_router(get_collection_router())
app.include_router(get_document_router())
app.include_router(get_all_documents_router())
app.include_router(get_phono_document_router())
app.include_router(get_auth_router())
app.include_router(get_user_router())
app.include_router(get_notification_router())
app.include_router(get_collection_comment_router())
app.include_router(get_gpt_router())
