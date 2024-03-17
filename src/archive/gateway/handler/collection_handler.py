import json

from uuid import uuid4
from fastapi import UploadFile, File, Form
from fastapi.exceptions import HTTPException
from pydantic import parse_obj_as

from src.archive.core import UnitOfWork
from src.archive.repository.collection import CollectionRepository
from src.archive.service.collection import CollectionService
from src.archive.gateway.schemas import CollectionRequest, CollectionResponse, CollectionUpdateRequest
from src.archive.database.engine import get_session

import time

service = CollectionService()

async def create_collection_handler(file: UploadFile = File(...), data: str = Form(...)):

    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="File is not in PDF format")

    try:
        data = json.loads(data)
        data["file_url"] = str(uuid4()) + "_"+ file.filename
        data = parse_obj_as(CollectionRequest, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing data: {str(e)}")

    collection = await service.create_collection(file=file.file.read(), data=data, uow=UnitOfWork(reposiotry=CollectionRepository, session_factory=get_session))

    response = CollectionResponse(
        id=collection.get_id,
        file_url=collection.get_file_url,
        theme=collection.get_theme,
        purpose=collection.get_purpose,
        task=collection.get_task,
        type_coll=collection.get_type_coll.name,
        class_coll=collection.get_class_coll.name,
        format_coll=collection.get_format_coll.name,
        method_coll=collection.get_method_coll.name,
        preface=collection.get_preface,
        note=collection.get_note,
        indication=collection.get_indication,
        intro_text=collection.get_intro_text,
        recommendations=collection.get_recommendations,
        created_at=collection.get_created_at
    )
    return response


async def get_collection_handler(id: int):
    collection = await service.get_collection(id=id, uow=UnitOfWork(reposiotry=CollectionRepository, session_factory=get_session))

    response = CollectionResponse(
        id=collection.get_id,
        file_url=collection.get_file_url,
        theme=collection.get_theme,
        purpose=collection.get_purpose,
        task=collection.get_task,
        type_coll=collection.get_type_coll.name,
        class_coll=collection.get_class_coll.name,
        format_coll=collection.get_format_coll.name,
        method_coll=collection.get_method_coll.name,
        preface=collection.get_preface,
        note=collection.get_note,
        indication=collection.get_indication,
        intro_text=collection.get_intro_text,
        recommendations=collection.get_recommendations,
        created_at=collection.get_created_at
    )
    return response

async def get_list_collecti0n_handler():
    collections = await service.get_list_collection(uow=UnitOfWork(reposiotry=CollectionRepository, session_factory=get_session))
    response = [
        CollectionResponse(
            id=collection.get_id,
            file_url=collection.get_file_url,
            theme=collection.get_theme,
            purpose=collection.get_purpose,
            task=collection.get_task,
            type_coll=collection.get_type_coll.name,
            class_coll=collection.get_class_coll.name,
            format_coll=collection.get_format_coll.name,
            method_coll=collection.get_method_coll.name,
            preface=collection.get_preface,
            note=collection.get_note,
            indication=collection.get_indication,
            intro_text=collection.get_intro_text,
            recommendations=collection.get_recommendations,
            created_at=collection.get_created_at
    ) for collection in collections]

    return response

async def update_colelction_handler(id: int, file: UploadFile = File(None), data: str = Form(...)):

    data = json.loads(data)

    if file:
        if file.content_type != 'application/pdf':
            raise HTTPException(status_code=400, detail="File is not in PDF format")
        
        data["file_url"] = str(uuid4()) + "_"+ file.filename    
    else:
        data["file_url"] = None
            
        
    try:
        data = parse_obj_as(CollectionUpdateRequest, data)
        file = file.file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing data: {str(e)}")
    
    collection = await service.update_collection(id=id, data=data, file=file, uow=UnitOfWork(reposiotry=CollectionRepository, session_factory=get_session))

    
    response = CollectionResponse(
        id=collection.get_id,
        file_url=collection.get_file_url,
        theme=collection.get_theme,
        purpose=collection.get_purpose,
        task=collection.get_task,
        type_coll=collection.get_type_coll.name,
        class_coll=collection.get_class_coll.name,
        format_coll=collection.get_format_coll.name,
        method_coll=collection.get_method_coll.name,
        preface=collection.get_preface,
        note=collection.get_note,
        indication=collection.get_indication,
        intro_text=collection.get_intro_text,
        recommendations=collection.get_recommendations,
        created_at=collection.get_created_at
    )

    return response

async def delete_collection_handler(id: int):
    await service.delete_class_collection(id=id, uow=UnitOfWork(reposiotry=CollectionRepository, session_factory=get_session))

    return ["Delete success"]