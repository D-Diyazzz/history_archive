import json

from uuid import uuid4
from typing import List
from fastapi import UploadFile, File, Form, Depends
from fastapi.exceptions import HTTPException
from pydantic import parse_obj_as

from src.archive.core import UnitOfWork
from src.archive.repository.document import DocumentRepository
from src.archive.service.document import DocumentService
from src.archive.gateway.schemas import DocumentRequest, DocumentResponse, DocumentUpdateRequest, SearchDataResponse
from src.archive.database.engine import get_session, init_engine
from src.archive.dependencies.auth_dependencies import check_access_token, check_role
from src.archive.gateway.converter import DocumentConverter
from src.archive.views import DocumentViews


service = DocumentService()
allowed_formats = ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "image/png", "image/jpeg", "image/webp", "image/jpg"]

async def create_document_handler(user_data = Depends(check_role), files: List[UploadFile] = File(...), data: str = Form(...)):
    files_dict = {}
    for file in files:
        if file.content_type not in allowed_formats:
            raise HTTPException(status_code=400, detail=f"Unsupported format {file.content_type}. Allowed formats: png, jpg, jpeg, doc, docs, pdf")
        filename = str(uuid4()) + "_"+ file.filename 
        files_dict[filename] = await file.read()
    try:
        data = json.loads(data)
        data = parse_obj_as(DocumentRequest, data)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"Error parsing data: {str(e)}")
    
    document = await service.create_document(files=files_dict, data=data, uow=UnitOfWork(reposiotry=DocumentRepository, session_factory=get_session))

    response = DocumentConverter.model_to_document(document=document)

    return response


async def get_document_handler(id: int):

    document = await DocumentViews.get_document_by_id_view(id=id, engine=init_engine())

    return document


async def get_list_document_handler(user_data = Depends(check_access_token)):

    documents = await DocumentViews.get_documents_view(engine=init_engine())

    return documents


async def remove_files_handler(id: int, data: List[str]):
    document = await service.remove_file_in_document(id=id, files=data,uow=UnitOfWork(reposiotry=DocumentRepository, session_factory=get_session))

    response = DocumentConverter.model_to_document(document=document)

    return response

async def update_document_handler(id: int,  files: List[UploadFile] = File(None),data: str = Form(...)):
    data = json.loads(data)
    files_dict = {}
    if files:
        for file in files:
            if file.content_type not in allowed_formats:
                raise HTTPException(status_code=400, detail=f"Unsupported format {file.content_type}. Allowed formats: png, jpg, jpeg, doc, docs, pdf")
            filename = str(uuid4()) + "_"+ file.filename 
            files_dict[filename] = await file.read()            
    
    try:
        data = parse_obj_as(DocumentUpdateRequest, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing data: {str(e)}")
    
    document = await service.update_document(id=id, data=data, files=files_dict, uow=UnitOfWork(reposiotry=DocumentRepository, session_factory=get_session))

    response = DocumentConverter.model_to_document(document=document)

    return response


async def delete_document_handler(id: int):
    await service.delete_document(id=id, uow=UnitOfWork(reposiotry=DocumentRepository, session_factory=get_session))

    return ["Delete success"]
