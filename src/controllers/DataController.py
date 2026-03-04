from .BaseController import BaseController
from fastapi import UploadFile, HTTPException
from helpers.config import Settings
from models.enums import ResponseSignal
from .ProjectController import ProjectController
import re
import os

class DataController(BaseController):
    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.file_to_scale = 1048576

    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.Settings.FILE_ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail=ResponseSignal.FILE_TYPE_ERROR.value)
        
        if file.size > self.Settings.MAX_FILE_SIZE * self.file_to_scale:
            raise HTTPException(status_code=400, detail=ResponseSignal.FILE_SIZE_ERROR.value)
        
        return True, {"signal": ResponseSignal.FILE_VALIDATED_SUCCESSFULLY.value}
    
    
    def generate_unique_file_path(self, original_file_name: str, project_id: str):

        random_key = self.generate_random_string()
        project_path = ProjectController(self.Settings).get_project_path(project_id=project_id)

        cleaned_file_name = self.get_clean_file_name(original_file_name=original_file_name)
        new_file_path = os.path.join(project_path, random_key+"_"+cleaned_file_name)

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(project_path, random_key+"_"+cleaned_file_name)

        return new_file_path, random_key+"_"+cleaned_file_name


   
    def get_clean_file_name(self, original_file_name: str):
        # strip and remove spaces
        cleaned_file_name = original_file_name.strip()
        # replace spaces with underscores first
        cleaned_file_name = cleaned_file_name.replace(" ", "_")
        # remove anything else that is not alphanumeric or dots
        cleaned_file_name = re.sub(r'[^\w.]', '', cleaned_file_name)
        return cleaned_file_name
        