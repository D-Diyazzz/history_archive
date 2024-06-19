from .type_handlers import (
    create_type_handler, 
    get_list_of_types_handler,
    get_type_collection_handler,
    delete_type_collection_handler
)

from .class_collection_handlers import (
    create_class_collection_handler,
    get_class_collection_handler,
    get_list_class_collection_handler,
    delete_class_collection_handler,
)

from .form_collection_handler import (
    create_form_collection_handler,
    get_form_collection_handler,
    get_list_form_collection_handler,
    delete_form_collection_handler,
)

from .method_collection_handler import (
    create_method_collection_handler,
    get_list_method_collection_handler,
    get_method_collection_handler,
    delete_method_collection_handler,
)

from .collection_handler import (
    create_collection_handler,
    get_collection_handler,
    get_list_collecti0n_handler,
    update_colelction_handler,
    delete_collection_handler,
)

from .document_handler import(
    create_document_handler,
    get_document_handler,
    get_list_document_handler,
    update_document_handler,
    delete_document_handler,
    remove_files_handler,
)

from .auth_handler import(
    registration_handler,
    login_handler,
    refresh_token_handler,
)


__all__ = [
    "create_type_handler",
    "get_list_of_types_handler",
    "get_type_collection_handler",
    "delete_type_collection_handler",
    "create_class_collection_handler",
    "get_class_collection_handler",
    "get_list_class_collection_handler",
    "delete_class_collection_handler",
    "create_form_collection_handler",
    "get_form_collection_handler",
    "get_list_form_collection_handler",
    "delete_form_collection_handler",
    "create_method_collection_handler",
    "get_list_method_collection_handler",
    "get_method_collection_handler",
    "delete_method_collection_handler",
    "create_collection_handler",
    "get_collection_handler",
    "get_list_collecti0n_handler",
    "update_colelction_handler",
    "delete_collection_handler",
    "create_document_handler",
    "get_document_handler",
    "get_list_document_handler",
    "update_document_handler",
    "delete_document_handler",
    "remove_files_handler",

    "registration_handler",
    "login_handler",
    "refresh_token_handler",
]
