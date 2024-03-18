import json

from uuid import uuid4
from fastapi import UploadFile, File, Form
from fastapi.exceptions import HTTPException
from pydantic import parse_obj_as

from src.archive.core import UnitOfWork
from src.archive.repository.document import DocumentRepository
from src.archive.service.document import DocumentService
from src.archive.gateway.schemas import DocumentRequest, DocumentResponse, DocumentUpdateRequest
from src.archive.database.engine import get_session


service = DocumentService()

async def create_document_handler(file: UploadFile = File(...), data: str = Form(...)):
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="File is not in PDF format")

    try:
        data = json.loads(data)
        data["file_url"] = str(uuid4()) + "_"+ file.filename
        data = parse_obj_as(DocumentRequest, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing data: {str(e)}")


    document = await service.create_document(file=file.file.read(), data=data, uow=UnitOfWork(reposiotry=DocumentRepository, session_factory=get_session))

    response = DocumentResponse(
        id=document.get_id,
        file_url=document.get_file_url,
        title=document.get_title,
        heading=document.get_heading,
        author=document.get_author,
        description_content=document.get_description_content,
        dating=document.get_dating,
        legends=document.get_legends,
        format_doc=document.get_format_doc,
        color_palette=document.get_color_palette,
        resolution=document.get_resolution,
        compression=document.get_compression,
        scanner_model=document.get_scanner_model,
        created_at=document.get_created_at
    )

    return response


async def get_document_handler(id: int):
    document = await service.get_document(id=id, uow=UnitOfWork(reposiotry=DocumentRepository, session_factory=get_session))

    response = DocumentResponse(
        id=document.get_id,
        file_url=document.get_file_url,
        title=document.get_title,
        heading=document.get_heading,
        author=document.get_author,
        description_content=document.get_description_content,
        dating=document.get_dating,
        legends=document.get_legends,
        format_doc=document.get_format_doc,
        color_palette=document.get_color_palette,
        resolution=document.get_resolution,
        compression=document.get_compression,
        scanner_model=document.get_scanner_model,
        created_at=document.get_created_at
    )

    return response


async def get_list_document_handler():
    documents = await service.get_list_document(uow=UnitOfWork(reposiotry=DocumentRepository, session_factory=get_session))

    response = [
        DocumentResponse(
            id=document.get_id,
            file_url=document.get_file_url,
            title=document.get_title,
            heading=document.get_heading,
            author=document.get_author,
            description_content=document.get_description_content,
            dating=document.get_dating,
            legends=document.get_legends,
            format_doc=document.get_format_doc,
            color_palette=document.get_color_palette,
            resolution=document.get_resolution,
            compression=document.get_compression,
            scanner_model=document.get_scanner_model,
            created_at=document.get_created_at
    ) for document in documents]

    return response


async def update_document_handler(id: int, file: UploadFile = File(None), data: str = Form(...)):
    data = json.loads(data)

    if file:
        if file.content_type != 'application/pdf':
            raise HTTPException(status_code=400, detail="File is not in PDF format")
        
        data["file_url"] = str(uuid4()) + "_"+ file.filename    
        file = file.file.read()
    else:
        data["file_url"] = None
            
        
    try:
        data = parse_obj_as(DocumentUpdateRequest, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing data: {str(e)}")
    
    document = await service.update_document(id=id, data=data, file=file, uow=UnitOfWork(reposiotry=DocumentRepository, session_factory=get_session))

    response = DocumentResponse(
        id=document.get_id,
        file_url=document.get_file_url,
        title=document.get_title,
        heading=document.get_heading,
        author=document.get_author,
        description_content=document.get_description_content,
        dating=document.get_dating,
        legends=document.get_legends,
        format_doc=document.get_format_doc,
        color_palette=document.get_color_palette,
        resolution=document.get_resolution,
        compression=document.get_compression,
        scanner_model=document.get_scanner_model,
        created_at=document.get_created_at
    )

    return response


async def delete_document_handler(id: int):
    await service.delete_document(id=id, uow=UnitOfWork(reposiotry=DocumentRepository, session_factory=get_session))

    return ["Delete success"]