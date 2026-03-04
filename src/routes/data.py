from fastapi import APIRouter, FastAPI, Depends, UploadFile
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
from models.enums import ResponseSignal
import aiofiles
import os
import logging
from routes.schemas.data import ProcessRequest

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
prefix = "/api/v1/data",
tags= ["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile,
                      settings: Settings = Depends(get_settings)):
    
    data_controller = DataController(settings)
    validated, signal = data_controller.validate_uploaded_file(file)

    project_path = ProjectController(settings).get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_file_path(original_file_name=file.filename, project_id=project_id)
    
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"File upload failed: {str(e)}")
        return {
            "signal": ResponseSignal.FILE_UPLOAD_FAILED.value,  
            "validation_info": signal,
            
        }
    
    return {
        "signal": ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value,  
        "validation_info": signal,
        "file_id": file_id
    }


@data_router.post("/process/{project_id}")
async def process_data(project_id: str, request: ProcessRequest,
                       settings: Settings = Depends(get_settings)):
    file_id = request.file_id
    chunk_size = request.chunk_size
    chunk_overlap = request.chunk_overlap

    process_controller = ProcessController(project_id, settings)
    file_content = process_controller.get_file_content(file_id=file_id)
    file_chunks = process_controller.process_file_content(file_content, file_id, chunk_size, chunk_overlap)

    if file_chunks is None:
        return {
            "signal": ResponseSignal.FILE_PROCESSING_FAILED.value,
           
        }
    
    return {
        "signal": ResponseSignal.FILE_PROCESSING_SUCCESSFULLY.value,
        "file_id": file_id,
        "file_chunks": file_chunks
    }
