from fastapi import APIRouter

from src.archive.gateway.handler import (
    create_collection_handler,
    open_session_handler,
    get_collection_admin_handler,
    edit_collection_handler,
    pin_document_to_collection_handler,
    delete_document_link_handler,
    bind_user_to_collection_handler,

    create_document_handler,
    get_document_handler,
    get_list_document_handler,
    update_document_handler,
    delete_document_handler,
    remove_files_handler,

    registration_handler,
    login_handler,
    refresh_token_handler,

    get_admin_users_handler,
)


def get_collection_router() -> APIRouter:
    router = APIRouter(tags=["Collection"], prefix="/v1")
    router.post("/collection", status_code=201)(create_collection_handler)
    router.get("/collection/{id}/admin", status_code=200)(get_collection_admin_handler)
    router.post("/collection/{id}/session", status_code=200)(open_session_handler)
    router.patch("/collection/{id}", status_code=200)(edit_collection_handler)
    router.post("/collection/{id}/document", status_code=200)(pin_document_to_collection_handler)
    router.delete("/collection/{id}/document", status_code=200)(delete_document_link_handler)
    router.post("/collection/{id}/sci_group", status_code=200)(bind_user_to_collection_handler)
    return router

def get_document_router() -> APIRouter:
    router = APIRouter(tags=["Document"], prefix="/v1")
    router.post("/document", status_code=201)(create_document_handler)
    router.get("/document", status_code=200)(get_list_document_handler)
    router.get("/document/{id}", status_code=200)(get_document_handler)
    router.patch("/document/{id}", status_code=200)(update_document_handler)
    router.delete("/document/{id}/file", status_code=200)(remove_files_handler)
    router.delete("/document/{id}", status_code=202)(delete_document_handler)
    return router

def get_auth_router() -> APIRouter:
    router = APIRouter(tags=["Auth"], prefix="/v1")
    router.post("/register", status_code=201)(registration_handler)
    router.post("/login", status_code=200)(login_handler)
    router.post("/refresh-token", status_code=200)(refresh_token_handler)
    return router

def get_user_router() -> APIRouter:
    router = APIRouter(tags=["User"], prefix="/v1")
    router.get("/user/admin", status_code=200)(get_admin_users_handler)
    return router
