from sys import prefix
from fastapi import APIRouter

from src.archive.gateway.handler import (
    create_collection_handler,
    open_session_handler,
    get_collection_admin_handler,
    edit_collection_handler,
    pin_document_to_collection_handler,
    delete_document_link_handler,
    bind_user_to_collection_handler,
    del_bind_user_from_collection_handler,
    approve_collection_by_sci_user,
    approve_collection_by_admin_redactor_user_handler,
    get_user_collection_comment_handler,
    get_user_collection_comment_by_user_id_handler,
    get_collection_list_admin_panel_handler,
    delete_collection_handler,

    edit_collection_handler,

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
    get_sci_users_handler,
    get_redactor_users_handler,
    change_user_role_handler,
    get_all_users_handler,

    get_notifications_handler,
    read_collection_notification_handler,
)
from src.archive.gateway.handler.collection_comment_handler import edit_collection_comment_handler
from src.archive.gateway.handler.gpt_handler import get_response_from_question


def get_collection_router() -> APIRouter:
    router = APIRouter(tags=["Collection"], prefix="/v1")
    router.post("/collection", status_code=201)(create_collection_handler)
    router.get("/collection/{id}/admin", status_code=200)(get_collection_admin_handler)
    router.post("/collection/{id}/session", status_code=200)(open_session_handler)
    router.patch("/collection/{id}", status_code=200)(edit_collection_handler)
    router.post("/collection/{id}/document", status_code=200)(pin_document_to_collection_handler)
    router.delete("/collection/{id}/document", status_code=200)(delete_document_link_handler)
    router.post("/collection/{id}/user_group", status_code=200)(bind_user_to_collection_handler)
    router.delete("/collection/{id}/user_group", status_code=200)(del_bind_user_from_collection_handler)
    router.patch("/collection/{id}/sci_group", status_code=200)(approve_collection_by_sci_user)
    router.patch("/collection/{id}/approve", status_code=200)(approve_collection_by_admin_redactor_user_handler)
    router.get("/collection/{id}/comment", status_code=200)(get_user_collection_comment_handler)
    router.get("/collection/admin_list", status_code=200)(get_collection_list_admin_panel_handler)
    router.delete("/collection/{id}", status_code=200)(delete_collection_handler)
    return router

def get_collection_comment_router() -> APIRouter:
    router = APIRouter(tags=["Collection Comment"], prefix="/v1")
    router.patch("/collection/{id}/comment", status_code=200)(edit_collection_comment_handler)
    router.get("/collection/{id}/comment/{user_id}", status_code=200)(get_user_collection_comment_by_user_id_handler)
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
    router.get("/user/sci", status_code=200)(get_sci_users_handler)
    router.get("/user/redactor", status_code=200)(get_redactor_users_handler)
    router.patch("/user/role/{id}", status_code=200)(change_user_role_handler)
    router.get("/user", status_code=200)(get_all_users_handler)
    return router


def get_notification_router() -> APIRouter:
    router = APIRouter(tags=["Notification"], prefix="/v1")
    router.get("/notification/{id}", status_code=200)(get_notifications_handler)
    router.patch("/notification/{id}", status_code=200)(read_collection_notification_handler)
    return router


def get_gpt_router() -> APIRouter:
    router = APIRouter(tags=["Gpt"], prefix="/v1")
    router.post('/gpt', status_code=200)(get_response_from_question)
    return router
