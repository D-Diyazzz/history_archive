from fastapi import Depends

from src.archive.core import UnitOfWork
from src.archive.repository.Class_collection import ClassCollectionRepository
from src.archive.service.Class_collection import ClassCollectionService
from src.archive.gateway.schemas import ClassCollectionRequest, ClassCollectionResponse
from src.archive.database.engine import get_session
from src.archive.dependencies.auth_dependencies import chech_access_token, chech_role


service = ClassCollectionService()

async def create_class_collection_handler(data: ClassCollectionRequest):

    class_collection = await service.create_class_collection(data=data, uow=UnitOfWork(reposiotry=ClassCollectionRepository, session_factory=get_session))

    response = ClassCollectionResponse(
        id=class_collection.id,
        name=class_collection.name
    )

    return response


async def get_list_class_collection_handler(data = Depends(chech_access_token)):

    list_class_collection = await service.get_list_class_collection(uow=UnitOfWork(reposiotry=ClassCollectionRepository, session_factory=get_session))

    response = [
        ClassCollectionResponse(
            id=class_coll.get_id(),
            name=class_coll.get_name(),
        ) for class_coll in list_class_collection
    ]

    return response


async def get_class_collection_handler(id: int):

    class_collection = await service.get_class_collection(data=id, uow=UnitOfWork(reposiotry=ClassCollectionRepository, session_factory=get_session))

    response = ClassCollectionResponse(
        id=class_collection.get_id(),
        name=class_collection.get_name()
    )

    return response


async def delete_class_collection_handler(id: int):

    await service.delete_class_collection(data=id, uow=UnitOfWork(reposiotry=ClassCollectionRepository, session_factory=get_session))

    return ["Delete success"]