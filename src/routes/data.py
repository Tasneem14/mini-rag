from fastapi import APIRouter, FastAPI, Depends, UploadFile
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
from models.enums import ResponseSignal
import aiofiles
import os
import logging

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

    project_dir_path = ProjectController(settings).get_file_path(project_id=project_id)
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