from fastapi import APIRouter

from src.archive.gateway.handler import (
    create_type_handler, 
    get_list_of_types_handler,
    get_type_collection_handler,
    delete_type_collection_handler
)

def get_type_collection_router() -> APIRouter:
    router = APIRouter(tags=["Type collection"], prefix="/v1")
    router.post("/type-collection", status_code=201)(create_type_handler)
    router.get("/type-collection", status_code=200)(get_list_of_types_handler)
    router.get("/type-collection/{id}", status_code=200)(get_type_collection_handler)
    router.delete("/type-collection/{id}", status_code=202)(delete_type_collection_handler)
    return router