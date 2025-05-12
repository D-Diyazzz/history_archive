import json

from uuid import uuid4
from typing import List
from fastapi import UploadFile, File, Form, Depends
from fastapi.exceptions import HTTPException
from pydantic import parse_obj_as

from src.archive.core import UnitOfWork
from src.archive.gateway.converter.document_converter import PhotoDocumentConverter, VideoDocumentConverter
from src.archive.gateway.schemas.document_schemas import PhonoDocumentRequest, PhotoDocumentRequest, VideoDocumentRequest
from src.archive.repository.document import DocumentRepository
from src.archive.repository.document.phono_doc_repository import PhonoDocumentRepository
from src.archive.repository.document.photo_doc_repository import PhotoDocumentRepository
from src.archive.repository.document.video_doc_repository import VideoDocumentRepository
from src.archive.service.document import DocumentService
from src.archive.gateway.schemas import DocumentRequest, DocumentResponse, DocumentUpdateRequest, SearchDataResponse
from src.archive.database.engine import get_session, init_engine
from src.archive.dependencies.auth_dependencies import check_access_token, check_role
from src.archive.gateway.converter import DocumentConverter, PhonoDocumentConverter
from src.archive.service.document.phono_doc_service import PhonoDocumentService
from src.archive.service.document.photo_doc_service import PhotoDocumentService
from src.archive.service.document.video_doc_service import VideoDocumentService
from src.archive.views import DocumentViews


service = DocumentService()
allowed_formats = ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "image/png", "image/jpeg", "image/webp", "image/jpg"]
allowed_video_formats = [
    "video/mp4",               # .mp4
    "video/x-msvideo",         # .avi
    "video/x-matroska",        # .mkv
    "video/webm",              # .webm
    "video/quicktime",         # .mov
    "video/mpeg",              # .mpeg, .mpg
    "video/3gpp",              # .3gp
    "video/ogg",               # .ogv
    "application/vnd.apple.mpegurl",  # .m3u8 (HLS playlist)
    "video/mp2t"               # .ts (MPEG-TS)
]
allowed_image_formats = [
    "image/png",     # .png
    "image/jpeg",    # .jpeg, .jpg
    "image/jpg",     # .jpg (некоторые клиенты отправляют отдельно от image/jpeg)
    "image/webp",    # .webp
    "image/gif",     # .gif
    "image/bmp",     # .bmp
    "image/tiff"     # .tiff, .tif
]
allowed_audio_formats = [
    "audio/mpeg",       # .mp3
    "audio/wav",        # .wav
    "audio/x-wav",      # .wav (альтернативный MIME-тип)
    "audio/ogg",        # .ogg
    "audio/webm",       # .webm (может содержать аудио)
    "audio/mp4",        # .m4a
    "audio/x-aac",      # .aac
    "audio/flac"        # .flac
]



async def get_all_documents_handler(user_data=Depends(check_role)):
    documetns = await DocumentViews.get_all_documents_view(engine=init_engine())
    return documetns

async def create_document_handler(user_data = Depends(check_role), files: List[UploadFile] = File(None), data: str = Form(...)):
    files_dict = {}
    if files:
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


async def get_document_handler(id: str):

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




phono_service = PhonoDocumentService()

async def create_phono_document_handler(
        user_data = Depends(check_role), 
        files: List[UploadFile] = File(None),
        data: str = Form(...)
):
    files_dict = {}
    if files:
        for file in files:
            if file.content_type not in allowed_audio_formats:
                raise HTTPException(status_code=400, detail=f"Unsupported format {{file.content_type}}. Allowed formats: mp3, wav, ogg, webm, m4a, aac, flac"
)
            filename = str(uuid4()) + "_"+ file.filename 
            files_dict[filename] = await file.read()

    try:
        data = json.loads(data)
        data = parse_obj_as(PhonoDocumentRequest, data)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"Error parsing data: {str(e)}")

    document = await phono_service.create_document(
        files=files_dict,
        data=data,
        uow=UnitOfWork(reposiotry=PhonoDocumentRepository, session_factory=get_session)
    )
    
    response = PhonoDocumentConverter.model_to_document(document=document)

    return response


async def get_phono_document_handler(id: str):

    document = await DocumentViews.get_phono_document_by_id_view(id=id, engine=init_engine())
    return document 


async def get_list_phono_document_handler(user_data = Depends(check_access_token)):

    documents = await DocumentViews.get_phono_document(engine=init_engine())
    return documents



video_doc_service = VideoDocumentService()

async def create_videodocument_handler(user_data = Depends(check_role), files: List[UploadFile] = File(None), data: str = Form(...)):
    files_dict = {}
    if files:
        for file in files:
            if file.content_type not in allowed_video_formats:
                raise HTTPException(status_code=400, detail=f"Unsupported format {{file.content_type}}. Allowed formats: mp4, avi, mkv, webm, mov, mpeg, 3gp, ogv, m3u8, ts")
            filename = str(uuid4()) + "_"+ file.filename 
            files_dict[filename] = await file.read()

    try:
        data = json.loads(data)
        data = parse_obj_as(VideoDocumentRequest, data)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"Error parsing data: {str(e)}")
    
    document = await video_doc_service.create_document(files=files_dict, data=data, uow=UnitOfWork(reposiotry=VideoDocumentRepository, session_factory=get_session))
    response = VideoDocumentConverter.model_to_document(document=document)
    return response

async def get_video_document_handler(id: str):
    document = await DocumentViews.get_video_document_by_id_view(id=id, engine=init_engine())
    return document


async def get_list_video_document_handler(user_data = Depends(check_access_token)):
    documents = await DocumentViews.get_video_documents_view(engine=init_engine())
    return documents




photo_doc_service = PhotoDocumentService()

async def create_photodocument_handler(user_data = Depends(check_role), files: List[UploadFile] = File(None), data: str = Form(...)):
    files_dict = {}
    if files:
        for file in files:
            if file.content_type not in allowed_image_formats:
                raise HTTPException(status_code=400, detail=f"Unsupported format {{file.content_type}}. Allowed formats: png, jpg, jpeg, webp, gif, bmp, tiff")

            filename = str(uuid4()) + "_"+ file.filename 
            files_dict[filename] = await file.read()

    try:
        data = json.loads(data)
        data = parse_obj_as(PhotoDocumentRequest, data)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"Error parsing data: {str(e)}")
    
    document = await photo_doc_service.create_document(files=files_dict, data=data, uow=UnitOfWork(reposiotry=PhotoDocumentRepository, session_factory=get_session))
    response = PhotoDocumentConverter.model_to_document(document=document)
    return response


async def get_photo_document_handler(id: str):
    document = await DocumentViews.get_photo_document_by_id_view(id=id, engine=init_engine())
    return document


async def get_list_photo_document_handler(user_data = Depends(check_access_token)):
    documents = await DocumentViews.get_photo_documents_view(engine=init_engine())
    return documents

