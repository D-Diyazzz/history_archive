from src.archive.core import UnitOfWork
from src.archive.repository.Type import TypeRepository
from src.archive.service.Type import TypeServices
from src.archive.gateway.schemas import TypeResponse, TypeRequest
from src.archive.database.engine import get_session


service = TypeServices()

async def create_type_handler(data: TypeRequest):

    type_collection = await service.create_type(data=data, uow=UnitOfWork(reposiotry=TypeRepository, session_factory=get_session))

    response = TypeResponse(
        id=type_collection.id,
        name=type_collection.name
    )

    return response


async def get_list_of_types_handler():

    list_types = await service.get_list_of_type(uow=UnitOfWork(reposiotry=TypeRepository, session_factory=get_session))

    response = [
        TypeResponse(
            id=type_coll.id, 
            name=type_coll.name
        ) for type_coll in list_types
        ]
    
    return response


async def get_type_collection_handler(id: int):
    type_collection = await service.get_type_collection(data=id, uow=UnitOfWork(reposiotry=TypeRepository, session_factory=get_session))

    response = TypeResponse(
            id=type_collection.id,
            name=type_collection.name
    )

    return response


async def delete_type_collection_handler(id: int):
    await service.delete_type_collection(data=id,  uow=UnitOfWork(reposiotry=TypeRepository, session_factory=get_session))

    return ["Delete success"]