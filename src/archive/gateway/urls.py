from fastapi import APIRouter

from src.archive.gateway.handler import (
    create_type_handler, 
    get_list_of_types_handler,
    get_type_collection_handler,
    delete_type_collection_handler
)

from src.archive.gateway.handler import (
    create_class_collection_handler,
    get_class_collection_handler,
    get_list_class_collection_handler,
    delete_class_collection_handler,
)

def get_type_collection_router() -> APIRouter:
    router = APIRouter(tags=["Type collection"], prefix="/v1")
    router.post("/type-collection", status_code=201)(create_type_handler)
    router.get("/type-collection", status_code=200)(get_list_of_types_handler)
    router.get("/type-collection/{id}", status_code=200)(get_type_collection_handler)
    router.delete("/type-collection/{id}", status_code=202)(delete_type_collection_handler)
    return router


def get_class_collection_router() -> APIRouter:
    router = APIRouter(tags=["Class collection"], prefix="/v1")
    router.post("/class-collection", status_code=201)(create_class_collection_handler)
    router.get("/class-collection", status_code=200)(get_list_class_collection_handler)
    router.get("/class-collection/{id}", status_code=200)(get_class_collection_handler)
    router.delete("/class-collection/{id}", status_code=202)(delete_class_collection_handler)
    return router