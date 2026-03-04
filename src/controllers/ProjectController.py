from .BaseController import BaseController
from fastapi import UploadFile, HTTPException
from helpers.config import Settings
from models.enums import ResponseSignal
import os

class ProjectController(BaseController):
    def __init__(self, settings: Settings):
        super().__init__(settings)
    
    def get_project_path(self,project_id:str):
        project_path = os.path.join(self.files_path, project_id)
        
        if not os.path.exists(project_path):
           os.makedirs(project_path)
        return project_path