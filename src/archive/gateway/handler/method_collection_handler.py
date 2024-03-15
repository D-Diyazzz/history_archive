from src.archive.core import UnitOfWork
from src.archive.repository.Method_collection import MethodCollectionRepository
from src.archive.service.Method_collection import MethodCollectionService
from src.archive.gateway.schemas import FormCollectionResponse, FormCollectionRequest
from src.archive.database.engine import get_session


service = MethodCollectionService()

async def create_method_collection_handler(data: FormCollectionRequest):

    method_collection = await service.create_method_collection(data=data, uow=UnitOfWork(reposiotry=MethodCollectionRepository, session_factory=get_session))

    response = FormCollectionResponse(
        id=method_collection.id,
        name=method_collection.name
    )

    return response


async def get_list_method_collection_handler():

    list_method_collection = await service.get_list_method_collection( uow=UnitOfWork(reposiotry=MethodCollectionRepository, session_factory=get_session))

    response = [
        FormCollectionResponse(
            id=method_collection.get_id(),
            name=method_collection.get_name()
        ) for method_collection in list_method_collection
    ]

    return response


async def get_method_collection_handler(id: int):

    method_collection = await service.get_method_collection(data=id,  uow=UnitOfWork(reposiotry=MethodCollectionRepository, session_factory=get_session))

    response = FormCollectionResponse(
        id=method_collection.get_id(),
        name=method_collection.get_name(),
    )

    return response


async def delete_method_collection_handler(id: int):

    await service.delete_method_collection(data=id,  uow=UnitOfWork(reposiotry=MethodCollectionRepository, session_factory=get_session))

    return ["Delete success"]