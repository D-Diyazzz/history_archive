from src.archive.core import UnitOfWork
from src.archive.repository.Form_collection import FormCollectionRepository
from src.archive.service.Form_collection import FormCollectionService
from src.archive.gateway.schemas import FormCollectionResponse, FormCollectionRequest
from src.archive.database.engine import get_session


service = FormCollectionService()

async def create_form_collection_handler(data: FormCollectionRequest):

    form_collection = await service.create_form_collection(data=data, uow=UnitOfWork(reposiotry=FormCollectionRepository, session_factory=get_session))

    response = FormCollectionResponse(
        id=form_collection.id,
        name=form_collection.name
    )

    return response


async def get_list_form_collection_handler():

    list_form_collection = await service.get_list_form_collection( uow=UnitOfWork(reposiotry=FormCollectionRepository, session_factory=get_session))

    response = [
        FormCollectionResponse(
            id=form_collection.get_id(),
            name=form_collection.get_name()
        ) for form_collection in list_form_collection
    ]

    return response


async def get_form_collection_handler(id: int):

    form_collection = await service.get_form_collection(data=id,  uow=UnitOfWork(reposiotry=FormCollectionRepository, session_factory=get_session))

    response = FormCollectionResponse(
        id=form_collection.get_id(),
        name=form_collection.get_name(),
    )

    return response


async def delete_form_collection_handler(id: int):

    await service.delete_form_collection(data=id,  uow=UnitOfWork(reposiotry=FormCollectionRepository, session_factory=get_session))

    return ["Delete success"]