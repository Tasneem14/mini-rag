from .BaseController import BaseController
from .ProjectController import ProjectController
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models.enums import ProcessingEnum
from helpers.config import Settings
import os

class ProcessController(BaseController):
    def __init__(self, project_id: str, settings: Settings):
        super().__init__(settings)
        self.project_id = project_id
        self.project_path = ProjectController(self.Settings).get_project_path(project_id=self.project_id)

    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str):
        file_extension = self.get_file_extension(file_id=file_id)
        file_path = os.path.join(self.project_path, file_id)

        if file_extension ==ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf8")
        if file_extension ==ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        return None
    
    def get_file_content(self, file_id: str):
        loader = self.get_file_loader(file_id=file_id)
        if loader:
            return loader.load()
            
    def process_file_content(self, get_file_content: list, file_id: str, chunk_size: int=100, chunk_overlap: int=20):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", " "]
        )
        
        file_content_texts = [
            rec.page_content
            for rec in get_file_content
        ]
    
        file_content_metadata = [
            rec.metadata
            for rec in get_file_content
        ]

        chunks = text_splitter.create_documents(file_content_texts, metadatas=file_content_metadata)
        return chunks
        